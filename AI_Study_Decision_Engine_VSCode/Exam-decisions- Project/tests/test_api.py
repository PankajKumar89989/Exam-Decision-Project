from fastapi.testclient import TestClient

from api import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_local_decision_endpoint():
    payload = {
        "hours": 3,
        "exam_days": 2,
        "topics_remaining": 3,
        "difficulty": "High",
        "energy": "High",
        "important_topic": "Yes",
    }
    response = client.post("/api/decision", json=payload)
    assert response.status_code == 200
    assert response.json()["decision"] == "study_hard"
    assert response.json()["priority"] == "critical"
