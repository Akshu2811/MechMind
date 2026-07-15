"""Centralized logging configuration for MechMind.

Called from both the FastAPI app (app/main.py) and standalone scripts (e.g.
the ingestion CLI) so log formatting/levels are consistent no matter how the
code is run.
"""

from __future__ import annotations

import logging

LOG_FORMAT = "%(asctime)s %(levelname)-8s %(name)s: %(message)s"

_configured = False


def configure_logging(level: int = logging.INFO) -> None:
    global _configured
    if _configured:
        return
    logging.basicConfig(level=level, format=LOG_FORMAT)
    _configured = True
