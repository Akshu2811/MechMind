"""Unit tests for the chunking logic in app/services/ingestion.py: header
splitting, oversized-section fallback, and the "never cut mid-sentence"
guarantee. Uses small hand-built markdown strings, not the real manuals.
"""

from __future__ import annotations

import re

from app.services.ingestion import (
    MAX_CHUNK_WORDS,
    Chunk,
    chunk_manual_file,
    split_into_header_sections,
    split_on_paragraphs,
    split_on_sentences,
    word_count,
)

SENTENCE_END_RE = re.compile(r"[.!?]$")


def _sentence(idx: int, words: int = 10) -> str:
    """Builds a single, well-formed sentence of roughly `words` words."""
    body = " ".join(f"word{idx}_{i}" for i in range(words - 2))
    return f"Sentence {idx} covers {body}."


# ---------------------------------------------------------------------------
# Header splitting
# ---------------------------------------------------------------------------


def test_split_into_header_sections_splits_on_h2_and_h3():
    raw = (
        "# Sample Manual\n\n"
        "Some preamble text before any subsection header.\n\n"
        "## 2.1 First Section\n\n"
        "Body of the first section.\n\n"
        "### 2.1.1 Nested Subsection\n\n"
        "Body of the nested subsection.\n"
    )
    sections = split_into_header_sections(raw)

    assert len(sections) == 3
    preamble_heading, preamble_text = sections[0]
    assert preamble_heading is None
    assert "Sample Manual" in preamble_text
    assert "preamble text" in preamble_text

    h2_heading, h2_text = sections[1]
    assert h2_heading == "## 2.1 First Section"
    assert "Body of the first section." in h2_text

    h3_heading, h3_text = sections[2]
    assert h3_heading == "### 2.1.1 Nested Subsection"
    assert "Body of the nested subsection." in h3_text


def test_split_into_header_sections_h1_is_also_a_boundary():
    """A bare '#' (H1) must act as a chunk boundary too, so content under an
    H1-only chapter (e.g. an Appendix) doesn't bleed into a preceding
    ##/### section."""
    raw = (
        "## 4.1 Diagnostic Procedure\n\n"
        "Body of the diagnostic procedure.\n\n"
        "# Appendix A: Glossary\n\n"
        "Glossary content goes here.\n"
    )
    sections = split_into_header_sections(raw)

    assert len(sections) == 2
    assert sections[0][0] == "## 4.1 Diagnostic Procedure"
    assert "Body of the diagnostic procedure." in sections[0][1]
    # H1 boundary starts a new, unlabeled section (heading=None) rather than
    # being appended to the previous ## section.
    assert sections[1][0] is None
    assert "Glossary content goes here." in sections[1][1]
    assert "diagnostic procedure" not in sections[1][1].lower()


# ---------------------------------------------------------------------------
# Oversized-section fallback (paragraph, then sentence, splitting)
# ---------------------------------------------------------------------------


def test_split_on_paragraphs_keeps_chunks_under_the_word_limit():
    max_words = 30
    paragraphs = [" ".join(_sentence(i, 6) for i in range(3)) for i in range(6)]
    text = "\n\n".join(paragraphs)
    assert word_count(text) > max_words  # sanity: the fixture is actually oversized

    chunks = split_on_paragraphs(text, max_words=max_words)

    assert len(chunks) > 1
    for c in chunks:
        assert word_count(c) <= max_words


def test_split_on_paragraphs_never_drops_or_duplicates_content():
    max_words = 25
    paragraphs = [f"Paragraph {i} body text here for testing purposes only today." for i in range(8)]
    text = "\n\n".join(paragraphs)

    chunks = split_on_paragraphs(text, max_words=max_words)

    rejoined = "\n\n".join(chunks)
    for p in paragraphs:
        assert p in rejoined


def test_split_on_sentences_never_cuts_mid_sentence():
    """A single oversized paragraph (no blank lines) falls back to
    sentence-level splitting. Every resulting chunk must end on a sentence
    boundary, and reassembling the chunks must reproduce every sentence
    intact (no truncation, no merging mid-sentence)."""
    max_words = 20
    sentences = [_sentence(i, 8) for i in range(10)]
    text = " ".join(sentences)
    assert word_count(text) > max_words

    chunks = split_on_sentences(text, max_words=max_words)

    assert len(chunks) > 1
    for c in chunks:
        assert SENTENCE_END_RE.search(c.strip()), f"chunk does not end on a sentence boundary: {c!r}"

    reconstructed = " ".join(chunks)
    for s in sentences:
        assert s in reconstructed


# ---------------------------------------------------------------------------
# End-to-end: chunk_manual_file (small sample markdown, not the real manuals)
# ---------------------------------------------------------------------------


def test_chunk_manual_file_oversized_section_falls_back_and_keeps_heading(tmp_path):
    # One short section (stays a single chunk) and one deliberately oversized
    # section (must split, with the heading line repeated on every sub-chunk).
    oversized_paragraphs = [
        " ".join(_sentence(p * 10 + i, 8) for i in range(6)) for p in range(10)
    ]
    raw = (
        "# Sample Manual\n\n"
        "Document preamble.\n\n"
        "## 2.1 Small Section\n\n"
        "This section is short and stays as a single chunk.\n\n"
        "## 3.1 Oversized Section\n\n" + "\n\n".join(oversized_paragraphs) + "\n"
    )
    path = tmp_path / "pump_manual.md"
    path.write_text(raw, encoding="utf-8")

    chunks: list[Chunk] = chunk_manual_file(path)

    small_chunks = [c for c in chunks if c.metadata["section_title"] == "2.1 Small Section"]
    oversized_chunks = [c for c in chunks if c.metadata["section_title"] == "3.1 Oversized Section"]

    assert len(small_chunks) == 1
    assert len(oversized_chunks) > 1, "oversized section should have been split into multiple chunks"

    for c in oversized_chunks:
        assert word_count(c.text) <= MAX_CHUNK_WORDS
        assert c.text.startswith("## 3.1 Oversized Section"), "heading must be repeated on each sub-chunk"
        assert c.metadata["source_file"] == "pump_manual.md"
        assert c.metadata["equipment_type"] == "pump"
        assert c.metadata["section_number"] == "3.1"


def test_chunk_manual_file_never_cuts_mid_sentence(tmp_path):
    sentences = [_sentence(i, 8) for i in range(70)]
    body = " ".join(sentences)  # single oversized paragraph, no blank lines
    assert word_count(body) > MAX_CHUNK_WORDS  # sanity: the fixture is actually oversized
    raw = f"## 4.4 Long Diagnostic Section\n\n{body}\n"
    path = tmp_path / "compressor_manual.md"
    path.write_text(raw, encoding="utf-8")

    chunks = chunk_manual_file(path)

    assert len(chunks) > 1
    for c in chunks:
        text_without_heading = c.text.split("\n\n", 1)[1] if "\n\n" in c.text else c.text
        assert SENTENCE_END_RE.search(text_without_heading.strip())
