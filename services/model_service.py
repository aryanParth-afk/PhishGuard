import joblib
import streamlit as st


@st.cache_resource
def load_model():
    return joblib.load("phishguard_model.pkl")


def score_to_risk(score_raw):
    risk = 50 + (score_raw * 15)
    return max(0, min(100, risk))


def analyze_text(model, clean_input, mode, get_result_reason):
    score_raw = model.decision_function([clean_input])[0]
    risk = score_to_risk(score_raw)
    reason = get_result_reason(mode, clean_input, risk)
    trust_note = "This score is a model-based risk estimate, not a guaranteed probability."
    return risk, reason, trust_note


def analyze_url(clean_input, get_result_reason):
    risk = 10
    if "https" not in clean_input.lower():
        risk += 30
    if len(clean_input) > 60:
        risk += 20
    if any(x in clean_input.lower() for x in ["bit.ly", "verify", "update", "login"]):
        risk += 40

    reason = get_result_reason("url", clean_input, risk)
    trust_note = "This score is currently based on rule-based URL screening, not full model confidence."
    return risk, reason, trust_note