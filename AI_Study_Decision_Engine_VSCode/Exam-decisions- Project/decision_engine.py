def extract_answer(answer_data):
    if not isinstance(answer_data, dict):
        raise ValueError("Laya response is not a JSON object.")
    answers = answer_data.get("answers")
    if not isinstance(answers, dict):
        raise ValueError("Laya response does not contain a valid 'answers' object.")
    return answers


def build_decision(result):
    answers = extract_answer(result)
    decision_data = answers.get("decision", {})
    priority_data = answers.get("priority", {})
    if not isinstance(decision_data, dict) or not isinstance(priority_data, dict):
        raise ValueError("Laya response has an unexpected decision/priority format.")
    return {
        "decision": decision_data.get("choice", "unknown"),
        "priority": priority_data.get("score", "unknown"),
        "confidence": decision_data.get("confidence"),
        "probabilities": decision_data.get("probabilities", {}),
        "priority_probabilities": priority_data.get("probabilities", {}),
        "priority_confidence": priority_data.get("confidence"),
        "reasons": [],
    }


def build_local_decision(state):
    """Transparent heuristic demo; this is not a trained ML model."""
    hours = float(state["hours"])
    days = int(state["exam_days"])
    topics = int(state["topics_remaining"])
    difficulty = state["difficulty"]
    energy = state["energy"]
    important = state["important_topic"] == "Yes"
    reasons = []

    if energy == "Low":
        choice = "take_break"
        reasons.append("Your energy level is low; a short reset may help you focus.")
    elif topics == 0:
        choice = "revise"
        reasons.append("You reported no remaining topics, so reviewing covered material is a reasonable next step.")
    elif important and (days <= 3 or difficulty == "High"):
        choice = "study_hard"
        reasons.append("An important topic remains and the exam is close or the material is difficult.")
    elif difficulty == "High" and hours >= 2:
        choice = "study_hard"
        reasons.append("You have time available to make progress on a difficult topic.")
    elif difficulty == "Low" or hours < 1.5:
        choice = "study_easy"
        reasons.append("Starting with a manageable topic can help you use a short study window.")
    else:
        choice = "revise"
        reasons.append("A revision block is a practical default for your current inputs.")

    if days <= 2 or (topics >= 8 and days <= 7):
        priority = "critical"
        reasons.append("The exam is very close or many topics remain for the available time.")
    elif days <= 7 or (topics >= 5 and days <= 14):
        priority = "high"
        reasons.append("Your remaining preparation time suggests prioritising the next study block.")
    elif days <= 21:
        priority = "medium"
        reasons.append("There is some time to plan and work through the remaining material.")
    else:
        priority = "low"
        reasons.append("You have more time before the exam; keep a steady study schedule.")

    return {"decision": choice, "priority": priority, "confidence": None, "probabilities": {}, "reasons": reasons}
