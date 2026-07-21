"""Lightweight knowledge graph over MechMind's existing Qdrant data.

Builds a NetworkX graph in-memory from the same `mechmind_knowledge`
collection ingestion.py already populates -- no new database, no new
ingestion pass, no local `data/` reads (consistent with equipment_status.py,
this reads Qdrant so it also works on Render where `data/` isn't shipped).

Node types: Equipment, Document, AlarmCode, LogEntry.
Edge types: Equipment--described_in-->Document, Equipment--had_event-->LogEntry,
LogEntry--involves-->AlarmCode, Document--documents-->AlarmCode.

Manual chunks don't carry `alarm_code` or `equipment_id` payload fields
(only `equipment_type`), so `described_in` and `documents` edges are joined
via `equipment_type` -- the one field both manual chunks and log chunks
share -- rather than any new text parsing.
"""

from __future__ import annotations

from collections import defaultdict

import networkx as nx
from qdrant_client import QdrantClient

from app.services.equipment_status import _extract_severity
from app.services.ingestion import COLLECTION_NAME, get_qdrant_client

SCROLL_BATCH = 256


def _node_id(node_type: str, key: str) -> str:
    return f"{node_type}:{key}"


def _equipment_type_of(equipment_id: str) -> str:
    return equipment_id.split("-")[0].lower()


def _fetch_all_payloads(client: QdrantClient) -> list[dict]:
    payloads: list[dict] = []
    offset = None
    while True:
        points, offset = client.scroll(
            collection_name=COLLECTION_NAME,
            with_payload=True,
            with_vectors=False,
            limit=SCROLL_BATCH,
            offset=offset,
        )
        payloads.extend(p.payload or {} for p in points)
        if offset is None:
            break
    return payloads


def build_graph(client: QdrantClient | None = None) -> nx.MultiDiGraph:
    client = client or get_qdrant_client()
    graph = nx.MultiDiGraph()

    # equipment_type -> Document node ids, and alarm_code -> equipment_type(s)
    # seen on log entries carrying that code -- the join keys used below to
    # add described_in/documents edges without any new parsing.
    docs_by_type: dict[str, set[str]] = defaultdict(set)
    equipment_types_by_alarm: dict[str, set[str]] = defaultdict(set)

    for payload in _fetch_all_payloads(client):
        source_file = payload.get("source_file")
        equipment_type = payload.get("equipment_type")
        log_id = payload.get("log_id")

        if log_id is None:
            # Manual chunk.
            if source_file:
                doc_node = _node_id("document", source_file)
                if doc_node not in graph:
                    graph.add_node(doc_node, type="Document", label=source_file)
                if equipment_type:
                    docs_by_type[equipment_type].add(doc_node)
            continue

        # Log chunk.
        equipment_id = payload.get("equipment_id")
        alarm_code = payload.get("alarm_code")
        severity = _extract_severity(payload.get("text", ""))

        log_node = _node_id("log", log_id)
        if log_node not in graph:
            graph.add_node(log_node, type="LogEntry", label=log_id)

        if equipment_id:
            eq_node = _node_id("equipment", equipment_id)
            if eq_node not in graph:
                graph.add_node(eq_node, type="Equipment", label=equipment_id)
            graph.add_edge(eq_node, log_node, type="had_event")

        if alarm_code:
            alarm_node = _node_id("alarm", alarm_code)
            if alarm_node not in graph:
                graph.add_node(alarm_node, type="AlarmCode", label=alarm_code, severity=severity)
            elif severity and not graph.nodes[alarm_node].get("severity"):
                graph.nodes[alarm_node]["severity"] = severity
            graph.add_edge(log_node, alarm_node, type="involves")
            if equipment_id:
                equipment_types_by_alarm[alarm_code].add(_equipment_type_of(equipment_id))

    for node, data in list(graph.nodes(data=True)):
        if data["type"] != "Equipment":
            continue
        equipment_id = node.split(":", 1)[1]
        for doc_node in docs_by_type.get(_equipment_type_of(equipment_id), ()):
            graph.add_edge(node, doc_node, type="described_in")

    for node, data in list(graph.nodes(data=True)):
        if data["type"] != "AlarmCode":
            continue
        alarm_code = node.split(":", 1)[1]
        for equipment_type in equipment_types_by_alarm.get(alarm_code, ()):
            for doc_node in docs_by_type.get(equipment_type, ()):
                graph.add_edge(doc_node, node, type="documents")

    return graph


def _equipment_subgraph(graph: nx.MultiDiGraph, equipment_id: str, depth: int = 2) -> nx.MultiDiGraph:
    """Forward-only BFS from the equipment node, depth 2 by default: reaches
    its documents/log entries (depth 1) and the alarm codes those reach
    (depth 2), without pulling in unrelated equipment that happens to share a
    document -- edges never point back from Document/AlarmCode to Equipment,
    so a successors-only walk can't cross over to another unit."""
    eq_node = _node_id("equipment", equipment_id)
    if eq_node not in graph:
        return nx.MultiDiGraph()

    nodes = {eq_node}
    frontier = {eq_node}
    for _ in range(depth):
        next_frontier: set[str] = set()
        for node in frontier:
            next_frontier.update(graph.successors(node))
        next_frontier -= nodes
        nodes.update(next_frontier)
        frontier = next_frontier

    return graph.subgraph(nodes)


def graph_to_dict(graph: nx.MultiDiGraph) -> dict:
    nodes = []
    for node_id, data in graph.nodes(data=True):
        node = {"id": node_id, "type": data["type"], "label": data["label"]}
        if data["type"] == "AlarmCode":
            node["severity"] = data.get("severity")
        nodes.append(node)

    edges = [
        {"source": u, "target": v, "type": data["type"]}
        for u, v, data in graph.edges(data=True)
    ]

    return {"nodes": nodes, "edges": edges}


def get_knowledge_graph(equipment: str | None = None) -> dict:
    graph = build_graph()
    if equipment:
        graph = _equipment_subgraph(graph, equipment)
    return graph_to_dict(graph)
