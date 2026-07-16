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
    groundedness: float | None = None
    relevance: float | None = None


class EquipmentStatusItem(BaseModel):
    equipment_id: str
    equipment_tag: str | None = None
    last_alarm_code: str | None = None
    last_event_date: str | None = None
    days_ago: int | None = None
    resolved: bool | None = None
    status: str


class EquipmentStatusResponse(BaseModel):
    units: list[EquipmentStatusItem]
