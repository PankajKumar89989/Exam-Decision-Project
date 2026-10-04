import os
import requests
from dotenv import load_dotenv

load_dotenv()

class LayaAPIError(Exception):
    """Raised when the Laya API cannot return a usable decision."""

class LayaClient:
    def __init__(self):
        self.api_key = os.getenv("LAYA_API_KEY")
        self.base_url = os.getenv("LAYA_BASE_URL", "https://api.laya.studio").rstrip("/")
        if not self.api_key:
            raise LayaAPIError("LAYA_API_KEY is missing. Add it to your local .env file, or run in local demo mode.")
        self.url = f"{self.base_url}/v1/systemone"
        self.headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

    def decide(self, state: str):
        payload = {
            "state": state,
            "questions": {
                "decision": {
                    "type": "choice",
                    "instructions": "What should the student do next?",
                    "criteria": {
                        "study_hard": "Study the hardest or most important topic immediately.",
                        "study_easy": "Study an easier topic first to build momentum.",
                        "revise": "Revise previously studied material.",
                        "take_break": "Take a short break before continuing.",
                    },
                },
                "priority": {
                    "type": "score",
                    "instructions": "How urgent is the student's study situation?",
                    "criteria": ["low", "medium", "high", "critical"],
                },
            },
        }
        try:
            response = requests.post(self.url, headers=self.headers, json=payload, timeout=30)
        except requests.exceptions.Timeout as exc:
            raise LayaAPIError("Laya API request timed out.") from exc
        except requests.exceptions.ConnectionError as exc:
            raise LayaAPIError("Could not connect to Laya API. Check your internet connection.") from exc
        except requests.exceptions.RequestException as exc:
            raise LayaAPIError(f"Network error: {exc}") from exc
        if not response.ok:
            try:
                data = response.json()
                detail = data.get("detail", data.get("error", "Unknown API error")) if isinstance(data, dict) else str(data)
            except ValueError:
                detail = response.text or "Unknown API error"
            raise LayaAPIError(f"Laya API error {response.status_code}: {detail}")
        try:
            data = response.json()
        except ValueError as exc:
            raise LayaAPIError("Laya returned an invalid JSON response.") from exc
        if not isinstance(data, dict):
            raise LayaAPIError("Laya returned an unexpected response format.")
        return data
