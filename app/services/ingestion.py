"""Document ingestion pipeline for MechMind.

Parses the equipment manuals (header-based chunking) and the maintenance log
CSV (row-based chunking), embeds every chunk, and stores the results in a
Qdrant collection with rich metadata payloads for later filtering/display.
"""

from __future__ import annotations

import csv
import logging
import random
import re
import textwrap
import uuid
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels

from app.config import get_settings

logger = logging.getLogger(__name__)

MANUALS_DIR = Path("data/manuals")
LOGS_CSV = Path("data/logs/maintenance_logs.csv")
COLLECTION_NAME = "mechmind_knowledge"
MAX_CHUNK_WORDS = 500
EMBED_BATCH_SIZE = 100

EQUIPMENT_TYPE_BY_FILENAME = {
    "pump_manual.md": "pump",
    "motor_manual.md": "motor",
    "compressor_manual.md": "compressor",
}

# Matches markdown "##" or "###" headers only (not "#" or "####+"). These are
# the ones that become *labeled* chunks (section_title/section_number).
HEADER_RE = re.compile(r"^(#{2,3})[ \t]+(.*)$")
# Matches a bare "#" (H1) header. These also act as chunk boundaries -- some
# chapters (Glossary, Appendix, Revision History) go straight from an H1 into
# body text/tables with no "##"/"###" beneath them, so without treating H1 as
# a boundary too, that content would silently bleed into whatever "##"/"###"
# chunk happened to be open beforehand.
H1_RE = re.compile(r"^#[ \t]+(.*)$")
# Leading numeric section number in a heading, e.g. "3.2" in "3.2 Summary Table"
# (also handles a trailing letter sub-suffix like "2.5a").
SECTION_NUMBER_RE = re.compile(r"^(\d+(?:\.\d+)*[a-z]?)(?=[ \t.]|$)")
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")


@dataclass
class Chunk:
    text: str
    metadata: dict = field(default_factory=dict)


def word_count(text: str) -> int:
    return len(text.split())


def infer_equipment_type(filename: str) -> str:
    return EQUIPMENT_TYPE_BY_FILENAME.get(filename, "unknown")


def clean_heading(line: str) -> str:
    return re.sub(r"^#{2,3}[ \t]*", "", line.strip()).strip()


def parse_section_number(heading_text: str) -> str | None:
    m = SECTION_NUMBER_RE.match(heading_text.strip())
    return m.group(1) if m else None


def is_meaningful_chunk(text: str) -> bool:
    """Filters out chunks that are just a markdown horizontal rule ("---")
    left over from paragraph-splitting, with no other content."""
    stripped = re.sub(r"^#{1,3}[ \t]*", "", text.strip())
    return bool(stripped.strip("-_* \t\n"))


# ---------------------------------------------------------------------------
# Header-based section splitting
# ---------------------------------------------------------------------------

def split_into_header_sections(raw_text: str) -> list[tuple[str | None, str]]:
    """Split markdown text on '##' / '###' headers.

    Returns a list of (heading_line_or_None, section_text) tuples. The first
    tuple has heading_line=None if there is preamble content (title, doc
    control table, etc.) before the first '##'/'###' header. Each
    section_text includes its own heading line, per the "include heading
    text" requirement.
    """
    lines = raw_text.splitlines()
    sections: list[tuple[str | None, list[str]]] = []
    current_heading: str | None = None
    current_lines: list[str] = []

    def flush() -> None:
        if current_lines:
            sections.append((current_heading, list(current_lines)))

    for line in lines:
        if HEADER_RE.match(line):
            flush()
            current_heading = line.strip()
            current_lines = [line]
        elif H1_RE.match(line):
            flush()
            current_heading = None  # unlabeled chapter-break section, like the leading preamble
            current_lines = [line]
        else:
            current_lines.append(line)
    flush()

    return [(h, "\n".join(l).strip()) for h, l in sections]


# ---------------------------------------------------------------------------
# Size-based sub-splitting (paragraph boundaries, sentence boundaries as a
# fallback for a single oversized paragraph) -- never mid-sentence.
# ---------------------------------------------------------------------------

def split_on_sentences(text: str, max_words: int = MAX_CHUNK_WORDS) -> list[str]:
    sentences = [s for s in SENTENCE_SPLIT_RE.split(text.strip()) if s.strip()]
    chunks: list[str] = []
    current: list[str] = []
    current_words = 0
    for sent in sentences:
        sw = word_count(sent)
        if current and current_words + sw > max_words:
            chunks.append(" ".join(current))
            current, current_words = [], 0
        current.append(sent)
        current_words += sw
    if current:
        chunks.append(" ".join(current))
    return chunks


def split_on_lines(text: str, max_words: int = MAX_CHUNK_WORDS) -> list[str]:
    """Fallback for oversized multi-line blocks (markdown tables, tight lists
    with no blank lines between items) -- splits between lines, which are
    already complete, atomic units (a full table row or list item), so this
    never cuts mid-sentence either."""
    lines = [l for l in text.split("\n") if l.strip()]
    chunks: list[str] = []
    current: list[str] = []
    current_words = 0
    for line in lines:
        lw = word_count(line)
        if lw > max_words:
            if current:
                chunks.append("\n".join(current))
                current, current_words = [], 0
            chunks.extend(split_on_sentences(line, max_words))
            continue
        if current and current_words + lw > max_words:
            chunks.append("\n".join(current))
            current, current_words = [], 0
        current.append(line)
        current_words += lw
    if current:
        chunks.append("\n".join(current))
    return chunks


def split_on_paragraphs(text: str, max_words: int = MAX_CHUNK_WORDS) -> list[str]:
    paragraphs = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    if not paragraphs:
        return [text.strip()] if text.strip() else []

    chunks: list[str] = []
    current: list[str] = []
    current_words = 0

    for para in paragraphs:
        pw = word_count(para)

        if pw > max_words:
            if current:
                chunks.append("\n\n".join(current))
                current, current_words = [], 0
            # A single paragraph itself exceeds the limit. If it's a
            # multi-line block (a table or a tight list with no blank lines
            # between items), split between lines first, since each line is
            # already a complete unit. Otherwise it's ordinary prose on one
            # line, so fall back to sentence-level splitting. Either way we
            # never cut mid-sentence.
            if "\n" in para.strip():
                chunks.extend(split_on_lines(para, max_words))
            else:
                chunks.extend(split_on_sentences(para, max_words))
            continue

        if current and current_words + pw > max_words:
            chunks.append("\n\n".join(current))
            current, current_words = [], 0

        current.append(para)
        current_words += pw

    if current:
        chunks.append("\n\n".join(current))

    return chunks


# ---------------------------------------------------------------------------
# Manual chunking
# ---------------------------------------------------------------------------

def chunk_manual_file(path: Path) -> list[Chunk]:
    raw_text = path.read_text(encoding="utf-8")
    equipment_type = infer_equipment_type(path.name)
    sections = split_into_header_sections(raw_text)

    chunks: list[Chunk] = []
    for heading_line, full_text in sections:
        if heading_line is None:
            title_match = re.search(r"^#[ \t]+(.+)$", full_text, re.MULTILINE)
            section_title = title_match.group(1).strip() if title_match else "Document Header"
            section_number = None
            texts = (
                [full_text.strip()]
                if word_count(full_text) <= MAX_CHUNK_WORDS
                else split_on_paragraphs(full_text)
            )
        else:
            section_title = clean_heading(heading_line)
            section_number = parse_section_number(section_title)

            if word_count(full_text) <= MAX_CHUNK_WORDS:
                texts = [full_text.strip()]
            else:
                body = "\n".join(full_text.splitlines()[1:]).strip()
                sub_bodies = split_on_paragraphs(body)
                texts = [f"{heading_line.strip()}\n\n{sb.strip()}".strip() for sb in sub_bodies]

        for t in texts:
            if not t.strip() or not is_meaningful_chunk(t):
                continue
            chunks.append(
                Chunk(
                    text=t.strip(),
                    metadata={
                        "source_file": path.name,
                        "section_title": section_title,
                        "section_number": section_number,
                        "equipment_type": equipment_type,
                    },
                )
            )

    return chunks


# ---------------------------------------------------------------------------
# Maintenance log chunking (one row = one chunk)
# ---------------------------------------------------------------------------

def chunk_maintenance_log(path: Path) -> list[Chunk]:
    chunks: list[Chunk] = []
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            text = (
                f"Log {row['log_id']} -- {row['equipment_id']} ({row['equipment_tag']}) "
                f"on {row['date']}: Alarm {row['alarm_code']} ({row['severity']}). "
                f"Technician notes: {row['technician_notes']} "
                f"Action taken: {row['action_taken']} "
                f"Downtime: {row['downtime_hours']} hours. Resolved: {row['resolved']}."
            )
            equipment_type = row["equipment_id"].split("-")[0].lower()
            chunks.append(
                Chunk(
                    text=text,
                    metadata={
                        "source_file": path.name,
                        "equipment_id": row["equipment_id"],
                        "alarm_code": row["alarm_code"],
                        "date": row["date"],
                        "log_id": row["log_id"],
                        "equipment_type": equipment_type,
                    },
                )
            )
    return chunks


def collect_all_chunks() -> list[Chunk]:
    chunks: list[Chunk] = []
    for manual_path in sorted(MANUALS_DIR.glob("*.md")):
        chunks.extend(chunk_manual_file(manual_path))
    if LOGS_CSV.exists():
        chunks.extend(chunk_maintenance_log(LOGS_CSV))
    return chunks


# ---------------------------------------------------------------------------
# Embedding
# ---------------------------------------------------------------------------

OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
OPENAI_EMBEDDING_DIM = 1536

GEMINI_EMBEDDING_MODEL = "models/text-embedding-004"
GEMINI_EMBEDDING_DIM = 768


class EmbeddingProvider:
    """Picks OpenAI or Gemini embeddings based on which API key is set in .env."""

    def __init__(self) -> None:
        settings = get_settings()
        if settings.OPENAI_API_KEY:
            from openai import OpenAI

            self.provider = "openai"
            self.model = OPENAI_EMBEDDING_MODEL
            self.dim = OPENAI_EMBEDDING_DIM
            self._client = OpenAI(api_key=settings.OPENAI_API_KEY)
        elif settings.GEMINI_API_KEY:
            import google.generativeai as genai

            self.provider = "gemini"
            self.model = GEMINI_EMBEDDING_MODEL
            self.dim = GEMINI_EMBEDDING_DIM
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self._genai = genai
        else:
            raise RuntimeError(
                "No embedding provider configured. Set OPENAI_API_KEY or "
                "GEMINI_API_KEY in .env before running ingestion."
            )

    def embed(self, texts: list[str], batch_size: int = EMBED_BATCH_SIZE) -> list[list[float]]:
        vectors: list[list[float]] = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            if self.provider == "openai":
                resp = self._client.embeddings.create(model=self.model, input=batch)
                vectors.extend(d.embedding for d in resp.data)
            else:
                for t in batch:
                    resp = self._genai.embed_content(model=self.model, content=t)
                    vectors.append(resp["embedding"])
        return vectors


# ---------------------------------------------------------------------------
# Qdrant storage
# ---------------------------------------------------------------------------

def get_qdrant_client() -> QdrantClient:
    settings = get_settings()
    return QdrantClient(url=settings.QDRANT_URL, api_key=settings.QDRANT_API_KEY)


def ensure_collection(client: QdrantClient, name: str, vector_size: int) -> None:
    """(Re)create the collection so re-running ingestion yields a consistent,
    duplicate-free point count that matches the freshly generated chunks."""
    if client.collection_exists(name):
        client.delete_collection(name)
    client.create_collection(
        collection_name=name,
        vectors_config=qmodels.VectorParams(size=vector_size, distance=qmodels.Distance.COSINE),
    )
    # Needed so retrieval.py can filter by equipment_type/source_file (e.g. to
    # guarantee manual-chunk coverage for equipment-specific queries).
    for field in ("equipment_type", "source_file"):
        client.create_payload_index(
            collection_name=name, field_name=field, field_schema=qmodels.PayloadSchemaType.KEYWORD
        )


def upsert_chunks(
    client: QdrantClient,
    collection_name: str,
    chunks: list[Chunk],
    vectors: list[list[float]],
    batch_size: int = EMBED_BATCH_SIZE,
) -> None:
    points = []
    for chunk, vector in zip(chunks, vectors):
        payload = dict(chunk.metadata)
        payload["text"] = chunk.text
        payload["word_count"] = word_count(chunk.text)
        points.append(qmodels.PointStruct(id=str(uuid.uuid4()), vector=vector, payload=payload))

    for i in range(0, len(points), batch_size):
        client.upsert(collection_name=collection_name, points=points[i : i + batch_size])


# ---------------------------------------------------------------------------
# Verification / summary
# ---------------------------------------------------------------------------

def log_summary(chunks: list[Chunk], qdrant_count: int) -> None:
    per_source = Counter(c.metadata["source_file"] for c in chunks)
    word_counts = [word_count(c.text) for c in chunks]

    lines = ["", "=" * 72, "INGESTION SUMMARY", "=" * 72, f"Total chunks created: {len(chunks)}"]

    lines.append("\nChunks per source file:")
    for src, count in sorted(per_source.items()):
        lines.append(f"  {src:30s} {count}")

    avg_words = sum(word_counts) / len(word_counts)
    lines.append(
        f"\nChunk word count -- avg: {avg_words:.1f}, "
        f"min: {min(word_counts)}, max: {max(word_counts)}"
    )

    lines.append(f"\nQdrant collection point count: {qdrant_count}")
    status = "MATCH" if qdrant_count == len(chunks) else "MISMATCH"
    lines.append(f"Verification: {status} (expected {len(chunks)}, got {qdrant_count})")

    lines.append("\n" + "-" * 72)
    lines.append("SAMPLE CHUNKS")
    lines.append("-" * 72)
    sample = random.sample(chunks, k=min(3, len(chunks)))
    for i, c in enumerate(sample, start=1):
        lines.append(f"\n[{i}] metadata: {c.metadata}")
        lines.append(f"    word_count: {word_count(c.text)}")
        lines.append("    text:")
        lines.append(textwrap.indent(c.text, "    "))
    lines.append("\n" + "=" * 72)

    logger.info("\n".join(lines))


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def run_ingestion() -> None:
    logger.info("Collecting and chunking source documents...")
    chunks = collect_all_chunks()
    logger.info("-> %d chunks created", len(chunks))

    logger.info("Initializing embedding provider...")
    try:
        embedder = EmbeddingProvider()
    except Exception:
        logger.error("Failed to initialize embedding provider", exc_info=True)
        raise
    logger.info("-> using %s (%s, dim=%d)", embedder.provider, embedder.model, embedder.dim)

    logger.info("Embedding chunks (batched)...")
    try:
        vectors = embedder.embed([c.text for c in chunks])
    except Exception:
        logger.error("Embedding request failed during ingestion", exc_info=True)
        raise
    logger.info("-> %d vectors generated", len(vectors))

    logger.info("Connecting to Qdrant and preparing collection...")
    try:
        client = get_qdrant_client()
        ensure_collection(client, COLLECTION_NAME, embedder.dim)

        logger.info("Upserting points into Qdrant...")
        upsert_chunks(client, COLLECTION_NAME, chunks, vectors)

        count_result = client.count(collection_name=COLLECTION_NAME, exact=True)
        qdrant_count = count_result.count
    except Exception:
        logger.error("Qdrant operation failed during ingestion", exc_info=True)
        raise

    log_summary(chunks, qdrant_count)


if __name__ == "__main__":
    from app.logging_config import configure_logging

    configure_logging()
    run_ingestion()
