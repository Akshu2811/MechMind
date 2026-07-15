"""Unit tests for the pure-logic pieces of app/services/retrieval.py:
equipment-ID detection and query/content intent classification. No Qdrant or
LLM calls -- these functions take plain strings/sets in and out.
"""

from __future__ import annotations

from app.services.retrieval import (
    classify_chunk_content_type,
    classify_query_intent,
    detect_equipment_id,
    equipment_type_for_id,
)

KNOWN_IDS = {"Pump-3", "Motor-1", "Compressor-2"}


# ---------------------------------------------------------------------------
# Equipment-ID detection
# ---------------------------------------------------------------------------


def test_detect_equipment_id_finds_exact_match():
    assert detect_equipment_id("Why is Pump-3 overheating?", KNOWN_IDS) == "Pump-3"


def test_detect_equipment_id_is_case_insensitive():
    assert detect_equipment_id("motor-1 vibration issue", KNOWN_IDS) == "Motor-1"


def test_detect_equipment_id_returns_none_when_absent():
    assert detect_equipment_id("What is the capital of France?", KNOWN_IDS) is None


def test_detect_equipment_id_respects_word_boundaries():
    """"Motor-10" must not spuriously match the known ID "Motor-1"."""
    assert detect_equipment_id("Motor-10 tripped on overload", KNOWN_IDS) is None


def test_equipment_type_for_id():
    assert equipment_type_for_id("Pump-3") == "pump"
    assert equipment_type_for_id("Motor-1") == "motor"
    assert equipment_type_for_id("Compressor-2") == "compressor"


# ---------------------------------------------------------------------------
# Query intent classification (alarm vs. context)
# ---------------------------------------------------------------------------


def test_classify_query_intent_detects_alarm_signal():
    query = "Compressor-2 fault code triggered a critical alarm"
    assert classify_query_intent(query) == "alarm"


def test_classify_query_intent_detects_context_signal():
    query = "What ambient temperature and sizing capacity affects installation?"
    assert classify_query_intent(query) == "context"


def test_classify_query_intent_returns_none_on_no_signal():
    assert classify_query_intent("Tell me about Motor-1") is None


def test_classify_query_intent_returns_none_on_tie():
    # One alarm keyword ("alarm"), one context keyword ("sizing") -> a tie.
    query = "Does the sizing guide mention an alarm for this unit?"
    assert classify_query_intent(query) is None


# ---------------------------------------------------------------------------
# Chunk content-type classification (section number -> alarm/context)
# ---------------------------------------------------------------------------


def test_classify_chunk_content_type_section_3_and_4_are_alarm():
    assert classify_chunk_content_type("3.2") == "alarm"
    assert classify_chunk_content_type("4.7") == "alarm"


def test_classify_chunk_content_type_section_6_is_context():
    assert classify_chunk_content_type("6.3") == "context"


def test_classify_chunk_content_type_other_sections_are_none():
    assert classify_chunk_content_type("2.1") is None
    assert classify_chunk_content_type(None) is None
