from pydantic import BaseModel


class AskRequest(BaseModel):
    question: str


class SourceInfo(BaseModel):
    source_file: str
    section_title: str | None = None
    score: float


class AskResponse(BaseModel):
    answer: str
    sources: list[SourceInfo] = []
    retrieved_chunk_count: int
