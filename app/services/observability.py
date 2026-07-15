"""Shared LangFuse client. Keys come through Settings (like every other
credential in this app) rather than SDK's own env-var lookup, since nothing
here calls load_dotenv() to populate os.environ from .env.

Observability must never take down the core /ask feature: every entry point
here (client construction, starting/using an observation, scoring, flushing)
is wrapped so a LangFuse failure is logged as a warning and swallowed rather
than propagated.
"""

from __future__ import annotations

import logging
from functools import lru_cache

from langfuse import Langfuse

from app.config import get_settings

logger = logging.getLogger(__name__)


class _NoOpSpan:
    """Stand-in for a LangFuse observation when tracing isn't available.
    `.update()` is the only method call sites use on the yielded span."""

    def update(self, *args, **kwargs) -> None:
        pass


class _SafeSpan:
    """Wraps a real LangFuse span so a failure in `.update()` (e.g. a
    network blip while attaching metadata) can't propagate into request
    handling code."""

    def __init__(self, span) -> None:
        self._span = span

    def update(self, *args, **kwargs) -> None:
        try:
            self._span.update(*args, **kwargs)
        except Exception:
            logger.warning("LangFuse span update failed; continuing.", exc_info=True)


@lru_cache
def get_langfuse_client() -> Langfuse | None:
    """Returns the LangFuse client, or None if it could not be constructed.
    Callers should go through `observation()`/`safe_flush()`/
    `safe_score_current_trace()` below rather than using this directly, so
    a missing/broken client degrades gracefully everywhere."""
    settings = get_settings()
    try:
        return Langfuse(
            public_key=settings.LANGFUSE_PUBLIC_KEY,
            secret_key=settings.LANGFUSE_SECRET_KEY,
            host=settings.LANGFUSE_HOST,
        )
    except Exception:
        logger.warning(
            "Could not initialize LangFuse client; observability disabled for this process.",
            exc_info=True,
        )
        return None


class observation:
    """Context manager wrapping `langfuse.start_as_current_observation`.

    If starting the observation fails (LangFuse unreachable, auth issue,
    client unavailable, etc.), logs a warning and yields a no-op span
    instead -- the wrapped business logic still runs normally and any
    exception it raises propagates unchanged. Only LangFuse's own
    enter/exit failures are swallowed.
    """

    def __init__(self, name: str, **kwargs) -> None:
        self._name = name
        self._kwargs = kwargs
        self._cm = None

    def __enter__(self) -> _NoOpSpan | _SafeSpan:
        langfuse = get_langfuse_client()
        if langfuse is None:
            return _NoOpSpan()
        try:
            self._cm = langfuse.start_as_current_observation(name=self._name, **self._kwargs)
            span = self._cm.__enter__()
            return _SafeSpan(span)
        except Exception:
            logger.warning(
                "LangFuse observation '%s' could not be started; continuing without tracing.",
                self._name,
                exc_info=True,
            )
            self._cm = None
            return _NoOpSpan()

    def __exit__(self, exc_type, exc, tb) -> bool:
        if self._cm is None:
            return False
        try:
            return bool(self._cm.__exit__(exc_type, exc, tb))
        except Exception:
            logger.warning(
                "LangFuse observation '%s' failed to close cleanly; continuing.",
                self._name,
                exc_info=True,
            )
            return False


def safe_score_current_trace(**kwargs) -> None:
    langfuse = get_langfuse_client()
    if langfuse is None:
        return
    try:
        langfuse.score_current_trace(**kwargs)
    except Exception:
        logger.warning("LangFuse score_current_trace failed; continuing.", exc_info=True)


def safe_flush() -> None:
    langfuse = get_langfuse_client()
    if langfuse is None:
        return
    try:
        langfuse.flush()
    except Exception:
        logger.warning("LangFuse flush failed; continuing.", exc_info=True)
