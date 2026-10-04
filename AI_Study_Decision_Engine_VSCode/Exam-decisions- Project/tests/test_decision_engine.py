import pytest
from decision_engine import build_decision, build_local_decision, extract_answer


def test_low_energy_suggests_break():
    result = build_local_decision({"hours": 3, "exam_days": 7, "topics_remaining": 4, "difficulty": "Medium", "energy": "Low", "important_topic": "No"})
    assert result["decision"] == "take_break"


def test_no_topics_suggests_revision_when_energy_ok():
    result = build_local_decision({"hours": 2, "exam_days": 20, "topics_remaining": 0, "difficulty": "Medium", "energy": "High", "important_topic": "No"})
    assert result["decision"] == "revise"


def test_important_difficult_topic_close_to_exam():
    result = build_local_decision({"hours": 3, "exam_days": 2, "topics_remaining": 3, "difficulty": "High", "energy": "High", "important_topic": "Yes"})
    assert result["decision"] == "study_hard"
    assert result["priority"] == "critical"


def test_build_decision_parses_api_response():
    result = build_decision({"answers": {"decision": {"choice": "revise", "confidence": 0.8, "probabilities": {"revise": 0.8}}, "priority": {"score": "medium"}}})
    assert result["decision"] == "revise"
    assert result["confidence"] == 0.8


def test_invalid_api_response_raises():
    with pytest.raises(ValueError):
        extract_answer({"unexpected": {}})
