import streamlit as st
import joblib
import plotly.graph_objects as go
import re
from urllib.parse import urlparse


# --- PAGE SETUP ---
st.set_page_config(page_title="PhishGuard", layout="wide")


# --- CLEAN ACADEMIC CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .main-title {
        font-family: 'Helvetica', sans-serif;
        color: #00d4ff;
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 10px;
    }
    .project-sub {
        text-align: center;
        color: #8892b0;
        font-style: italic;
        margin-bottom: 30px;
    }
    </style>
    """, unsafe_allow_html=True)


# --- LOAD MODEL ---
@st.cache_resource
def load_model():
    return joblib.load('phishguard_model.pkl')


model = load_model()


# --- HELPERS ---
def normalize_text(text):
    return re.sub(r"\s+", " ", text.strip())


def is_valid_url(text):
    try:
        parsed = urlparse(text.strip())
        return parsed.scheme in ("http", "https") and bool(parsed.netloc)
    except Exception:
        return False


def score_to_risk(score_raw):
    risk = 50 + (score_raw * 15)
    return max(0, min(100, risk))


def get_result_label(risk):
    if risk > 70:
        return "malicious"
    elif risk > 30:
        return "suspicious"
    return "safe"


def get_result_reason(mode, user_data, risk):
    if mode in ["email", "sms"]:
        if risk > 70:
            return "The text contains patterns commonly associated with phishing or spam-like communication."
        elif risk > 30:
            return "The text includes some suspicious language patterns, so it should be reviewed carefully."
        return "The text appears relatively benign based on the model's learned text patterns."
    else:
        reasons = []
        lower_url = user_data.lower()

        if "https" not in lower_url:
            reasons.append("it does not use HTTPS")
        if len(user_data) > 60:
            reasons.append("the URL is unusually long")
        if any(x in lower_url for x in ["bit.ly", "verify", "update", "login"]):
            reasons.append("it contains commonly abused phishing keywords")

        if reasons:
            return "This URL was flagged because " + ", ".join(reasons) + "."
        return "This URL did not trigger the current rule-based screening checks."


# --- GAUGE ---
def draw_gauge(score):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': "Risk Score", 'font': {'size': 18, 'color': '#00d4ff'}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': "#00d4ff"},
            'bar': {'color': "#00d4ff"},
            'steps': [
                {'range': [0, 50], 'color': 'rgba(0, 255, 0, 0.1)'},
                {'range': [50, 100], 'color': 'rgba(255, 0, 0, 0.1)'}
            ]
        }
    ))
    fig.update_layout(
        height=300,
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': "#ffffff"}
    )
    return fig


# --- SIDEBAR (College Project Info) ---
with st.sidebar:
    st.header("📌 Project Details")
    st.markdown("""
    **Project Name:** PhishGuard  
    **Field:** Cyber Security / ML  
    **Algorithm:** Passive-Aggressive Classifier  
    **Dataset:** UCI SMS Spam Collection  
    """)
    st.divider()
    st.markdown("### 👨‍💻 Developed By:")
    st.write("ARYAN PARTH")


# --- MAIN UI ---
st.markdown('<p class="main-title">PhishGuard: Phishing Detection System</p>', unsafe_allow_html=True)
st.markdown('<p class="project-sub">A Machine Learning approach to identifying malicious communications</p>', unsafe_allow_html=True)

tabs = st.tabs(["📧 Email Analysis", "💬 SMS Analysis", "🔗 URL Heuristics"])

for i, mode in enumerate(["email", "sms", "url"]):
    with tabs[i]:
        col1, col2 = st.columns([1.5, 1])

        with col1:
            if mode == "email":
                user_data = st.text_area(
                    "Input Text (Email)",
                    height=200,
                    placeholder="Paste email content to test the model..."
                )
            elif mode == "sms":
                user_data = st.text_input(
                    "Input Text (SMS)",
                    placeholder="Enter SMS text..."
                )
            else:
                user_data = st.text_input(
                    "Input URL",
                    placeholder="https://example-site.com"
                )

            analyze = st.button(f"Analyze {mode.upper()}")

        with col2:
            if analyze:
                clean_input = normalize_text(user_data) if user_data else ""

                if not clean_input:
                    st.warning("Please enter some content to analyze.")
                    st.stop()

                with st.spinner("Model processing..."):
                    try:
                        if mode in ["email", "sms"]:
                            score_raw = model.decision_function([clean_input])[0]
                            risk = score_to_risk(score_raw)
                            reason = get_result_reason(mode, clean_input, risk)
                            trust_note = "This score is a model-based risk estimate, not a guaranteed probability."

                        else:
                            if not is_valid_url(clean_input):
                                st.warning("Please enter a valid URL starting with http:// or https://")
                                st.stop()

                            risk = 10
                            if "https" not in clean_input.lower():
                                risk += 30
                            if len(clean_input) > 60:
                                risk += 20
                            if any(x in clean_input.lower() for x in ['bit.ly', 'verify', 'update', 'login']):
                                risk += 40

                            reason = get_result_reason(mode, clean_input, risk)
                            trust_note = "This score is currently based on rule-based URL screening, not full model confidence."

                        st.plotly_chart(draw_gauge(risk), use_container_width=True)

                        result_label = get_result_label(risk)
                        if result_label == "malicious":
                            st.error("Result: Potential Malicious Intent")
                        elif result_label == "suspicious":
                            st.warning("Result: Suspicious Activity Detected")
                        else:
                            st.success("Result: Likely Benign / Safe")

                        st.caption(reason)
                        st.info(trust_note)

                    except Exception as e:
                        st.error("Something went wrong while analyzing the input.")
                        st.exception(e)


# --- FOOTER ---
st.divider()
st.markdown("""
### 📊 Methodology
This project utilizes a **TF-IDF (Term Frequency-Inverse Document Frequency)** vectorization method to convert text into numerical features, followed by a **Passive-Aggressive Classifier**. This specific algorithm was chosen for its high efficiency in binary text classification tasks.

**Note:** Email and SMS analysis are model-based. URL analysis currently uses rule-based screening in this Phase 1 version.
""")