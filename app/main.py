from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.routes import router as api_router
from app.config import get_settings
from app.logging_config import configure_logging

configure_logging()

settings = get_settings()

app = FastAPI(title=settings.APP_NAME)

app.include_router(api_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


# Mounted last (and at "/") so the explicit API routes above always match
# first; anything else -- "/", "/index.html", future static assets -- falls
# through to the static frontend.
STATIC_DIR = Path(__file__).parent / "static"
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")
