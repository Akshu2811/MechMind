from fastapi import FastAPI

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
