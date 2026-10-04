import streamlit as st
from decision_engine import build_local_decision
from laya_client import LayaClient, LayaAPIError

st.set_page_config(page_title="AI Study Decision Engine", page_icon="📚", layout="centered")
st.title("📚 AI Study Decision Engine")
st.caption("A study-planning assistant for ABES students and other learners.")
st.write("Enter your current study situation to get a suggested next step and urgency level.")

with st.form("study_form"):
    hours = st.number_input("Hours available today", min_value=0.5, max_value=24.0, value=3.0, step=0.5)
    exam_days = st.number_input("Days remaining before exam", min_value=1, max_value=365, value=7, step=1)
    topics_remaining = st.number_input("Topics remaining", min_value=0, max_value=20, value=4, step=1)
    difficulty = st.selectbox("Overall difficulty", ["Low", "Medium", "High"])
    energy = st.selectbox("Current energy level", ["Low", "Medium", "High"])
    important_topic = st.selectbox("Important/high-weightage topic remaining?", ["Yes", "No"])
    use_api = st.checkbox("Use Laya API (requires a valid LAYA_API_KEY in .env)", value=False)
    submitted = st.form_submit_button("Make Study Decision", type="primary", use_container_width=True)

if submitted:
    state = {
        "hours": hours,
        "exam_days": int(exam_days),
        "topics_remaining": int(topics_remaining),
        "difficulty": difficulty,
        "energy": energy,
        "important_topic": important_topic,
    }
    try:
        with st.spinner("Preparing your study recommendation..."):
            if use_api:
                result = LayaClient().decide(
                    f"Hours available today: {hours}\nDays remaining before exam: {exam_days}\n"
                    f"Topics remaining: {topics_remaining}\nDifficulty: {difficulty}\n"
                    f"Energy: {energy}\nImportant topic remaining: {important_topic}"
                )
                from decision_engine import build_decision
                decision = build_decision(result)
                st.caption("Result source: Laya API")
            else:
                decision = build_local_decision(state)
                st.caption("Result source: local rule-based demo (not an external AI model)")

        labels = {
            "study_hard": "Study the hardest or most important topic",
            "study_easy": "Start with an easier topic to build momentum",
            "revise": "Revise previously studied material",
            "take_break": "Take a short break, then return to studying",
        }
        st.subheader("Your suggested next step")
        st.success(labels.get(decision["decision"], str(decision["decision"])))
        c1, c2 = st.columns(2)
        c1.metric("Priority", str(decision.get("priority", "unknown")).upper())
        confidence = decision.get("confidence")
        c2.metric("Confidence", f"{confidence:.0%}" if isinstance(confidence, (int, float)) else "N/A")
        st.subheader("Why this suggestion?")
        for reason in decision.get("reasons", []):
            st.write(f"- {reason}")
        if decision.get("probabilities"):
            with st.expander("Decision probabilities (when provided by the API)"):
                st.json(decision["probabilities"])
        if use_api:
            with st.expander("View raw API response"):
                st.json(result)
        st.info("Use this as a planning aid, not as a guarantee of exam performance. Adjust the plan to your syllabus and wellbeing.")
    except LayaAPIError as exc:
        st.error(str(exc))
        st.warning("Check your LAYA_API_KEY, API endpoint, account access/credits, and internet connection. You can uncheck the API option to run the local demo.")
    except (ValueError, KeyError, TypeError) as exc:
        st.error(f"Could not interpret the decision response: {exc}")
    except Exception as exc:
        st.error(f"Unexpected application error: {exc}")

with st.expander("About this project"):
    st.write("This educational project demonstrates a Streamlit interface, input validation, a local decision engine, optional API integration, and error handling.")
