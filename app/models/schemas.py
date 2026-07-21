from pydantic import BaseModel


class AskRequest(BaseModel):
    question: str


class SourceInfo(BaseModel):
    source_file: str
    section_title: str | None = None
    log_id: str | None = None
    alarm_code: str | None = None
    score: float


class AskResponse(BaseModel):
    answer: str
    sources: list[SourceInfo] = []
    retrieved_chunk_count: int
    groundedness: float | None = None
    relevance: float | None = None
    latency_ms: float
    model: str | None = None


class EquipmentStatusItem(BaseModel):
    equipment_id: str
    equipment_tag: str | None = None
    last_alarm_code: str | None = None
    last_event_date: str | None = None
    days_ago: int | None = None
    resolved: bool | None = None
    severity: str | None = None
    status: str


class EquipmentStatusResponse(BaseModel):
    units: list[EquipmentStatusItem]


class RecentActivityItem(BaseModel):
    equipment_id: str
    alarm_code: str | None = None
    date: str
    days_ago: int
    resolved: bool | None = None


class RecentActivityResponse(BaseModel):
    entries: list[RecentActivityItem]


class KnowledgeGraphNode(BaseModel):
    id: str
    type: str
    label: str
    severity: str | None = None


class KnowledgeGraphEdge(BaseModel):
    source: str
    target: str
    type: str


class KnowledgeGraphResponse(BaseModel):
    nodes: list[KnowledgeGraphNode]
    edges: list[KnowledgeGraphEdge]


class ComplianceItem(BaseModel):
    equipment_id: str
    equipment_type: str
    compliant: bool
    reasons: list[str] = []


class ComplianceResponse(BaseModel):
    units: list[ComplianceItem]
