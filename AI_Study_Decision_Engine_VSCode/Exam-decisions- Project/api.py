from __future__ import annotations

from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, Field

from decision_engine import build_local_decision


class StudyInput(BaseModel):
    hours: float = Field(..., gt=0)
    exam_days: int = Field(..., ge=1)
    topics_remaining: int = Field(..., ge=0)
    difficulty: str = Field(...)
    energy: str = Field(...)
    important_topic: str = Field(...)

    @property
    def state(self) -> dict[str, Any]:
        return {
            "hours": self.hours,
            "exam_days": self.exam_days,
            "topics_remaining": self.topics_remaining,
            "difficulty": self.difficulty,
            "energy": self.energy,
            "important_topic": self.important_topic,
        }


app = FastAPI(
    title="AI Study Decision Engine API",
    description="REST API for generating study recommendations from the local decision engine.",
    version="1.0.0",
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "AI Study Decision Engine API is running."}


@app.post("/api/decision")
def create_decision(payload: StudyInput) -> dict[str, Any]:
    decision = build_local_decision(payload.state)
    return {
        "decision": decision["decision"],
        "priority": decision["priority"],
        "confidence": decision.get("confidence"),
        "probabilities": decision.get("probabilities", {}),
        "reasons": decision.get("reasons", []),
        "source": "local-rule-based-demo",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=False)
