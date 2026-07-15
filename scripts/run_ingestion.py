"""Standalone entry point to run the MechMind document ingestion pipeline.

Usage:
    python scripts/run_ingestion.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.services.ingestion import run_ingestion

if __name__ == "__main__":
    run_ingestion()
