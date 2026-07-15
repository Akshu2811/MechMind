"""Standalone retrieval-only smoke test for the MechMind Qdrant knowledge base.

Embeds a hardcoded set of test queries with the same embedding provider used
during ingestion, searches the `mechmind_knowledge` Qdrant collection, and
prints the top-5 matches per query. No LLM is called -- this only exercises
retrieval.

Usage:
    python scripts/test_retrieval.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.services.ingestion import COLLECTION_NAME, EmbeddingProvider, get_qdrant_client

TOP_K = 5
SNIPPET_LEN = 150

TEST_QUERIES = [
    "Why is Pump-3 overheating?",
    "What is the recommended action for OIL_PRESS_03?",
    "Has Compressor-2 had recurring issues?",
    "What's the difference between DISCH_PRESS_LOW_07 as a fault versus a sizing issue?",
    "Tell me about Motor-1 vibration problems",
]


def run() -> None:
    print("Initializing embedding provider...")
    embedder = EmbeddingProvider()
    print(f"  -> using {embedder.provider} ({embedder.model}, dim={embedder.dim})")

    print("Connecting to Qdrant...")
    client = get_qdrant_client()

    for query in TEST_QUERIES:
        print("\n" + "=" * 100)
        print(f"QUERY: {query}")
        print("=" * 100)

        vector = embedder.embed([query])[0]
        results = client.query_points(
            collection_name=COLLECTION_NAME,
            query=vector,
            limit=TOP_K,
        ).points

        if not results:
            print("  (no results)")
            continue

        for rank, point in enumerate(results, start=1):
            payload = point.payload or {}
            source_file = payload.get("source_file", "?")
            section_title = payload.get("section_title", "?")
            text = payload.get("text", "")
            snippet = text[:SNIPPET_LEN].replace("\n", " ")
            if len(text) > SNIPPET_LEN:
                snippet += "..."

            print(f"\n  [{rank}] score={point.score:.4f}")
            print(f"      source_file:   {source_file}")
            print(f"      section_title: {section_title}")
            print(f"      text:          {snippet}")

    print("\n" + "=" * 100)
    print("Done.")


if __name__ == "__main__":
    run()
