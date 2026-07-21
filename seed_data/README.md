# seed_data/

This folder preserves the exact synthetic dataset used to build MechMind's Qdrant collection.

To rebuild from scratch: copy these files into `data/manuals/` and `data/logs/`, then run `scripts/run_ingestion.py`.

This is a reproducibility snapshot only — nothing in the application reads from `seed_data/` at runtime. The running app only ever touches `data/` (gitignored, read by `ingestion.py`) and Qdrant (the actual runtime source of truth).
