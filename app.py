import streamlit as st
import plotly.graph_objects as go

from utils.helpers import (
    normalize_text,
    is_valid_url,
    get_result_label,
    get_result_reason,
)
from services.model_service import (
    load_model,
    analyze_text,
    analyze_url,
)

# --- PAGE SETUP ---
st.set_page_config(
    page_title="PhishGuard | Phishing Detection System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- TOP-LEVEL UI STYLING ---
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #0b1220 0%, #111827 100%);
        color: #e5eef8;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }

    .block-container {
        padding-top: 2.2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    .hero-card {
        max-width: 980px;
        margin: 0 auto 1.5rem auto;
        padding: 1.7rem 1.8rem 1.35rem 1.8rem;
        border-radius: 22px;
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.88) 0%, rgba(17, 24, 39, 0.80) 100%);
        border: 1px solid rgba(148, 163, 184, 0.16);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.22);
    }

    .hero-inner {
        width: 100%;
        max-width: 760px;
        margin: 0 auto;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }

    .hero-badge {
        display: inline-block;
        padding: 0.45rem 0.9rem;
        border-radius: 999px;
        background: rgba(34, 197, 94, 0.12);
        border: 1px solid rgba(34, 197, 94, 0.28);
        color: #86efac;
        font-size: 0.85rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }

    .hero-title {
        margin: 0 0 0.7rem 0;
        color: #f8fafc;
        font-size: 2.7rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        line-height: 1.12;
        text-align: center;
    }

    .hero-subline {
        margin: 0 0 1.2rem 0;
        color: #cbd5e1;
        font-size: 1.02rem;
        line-height: 1.75;
        text-align: center;
        max-width: 620px;
    }

    .hero-meta {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 0.75rem;
        flex-wrap: wrap;
        width: 100%;
        margin-top: 0.1rem;
    }

    .hero-chip {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 0.42rem 0.8rem;
        border-radius: 999px;
        background: rgba(148, 163, 184, 0.10);
        border: 1px solid rgba(148, 163, 184, 0.14);
        color: #dbeafe;
        font-size: 0.84rem;
        font-weight: 600;
    }

    .hero-spacer {
        padding-top: 0.35rem;
        padding-bottom: 0.2rem;
    }

    [data-testid="stSidebar"] {
        background: #0f172a;
        border-right: 1px solid rgba(148, 163, 184, 0.12);
    }

    [data-testid="stSidebar"] .block-container {
        padding-top: 1.5rem;
    }

    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #f8fafc;
        letter-spacing: -0.01em;
    }

    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] li,
    [data-testid="stSidebar"] label {
        color: #cbd5e1;
        line-height: 1.55;
    }

    [data-testid="stSidebar"] .stCaption {
        color: #94a3b8;
    }

    div[data-testid="stTabs"] {
        margin-top: 0.2rem;
    }

    div[data-testid="stTabs"] [data-baseweb="tab-list"] {
        margin-bottom: 0.6rem;
        gap: 1rem;
    }

    div[data-testid="stTabs"] [data-baseweb="tab"] {
        font-weight: 600;
        padding-top: 0.2rem;
        padding-bottom: 0.2rem;
    }

    div[data-testid="stTabs"] [data-baseweb="tab-panel"] {
        padding-top: 0 !important;
    }

    div[data-testid="stButton"] > button {
        border-radius: 12px;
        font-weight: 700;
    }

    .result-box {
        margin-top: 1rem;
        padding: 1rem;
        border-radius: 16px;
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.72) 0%, rgba(17, 24, 39, 0.66) 100%);
        border: 1px solid rgba(148, 163, 184, 0.16);
    }

    @media (max-width: 768px) {
        .hero-card {
            padding: 1.35rem 1rem 1.1rem 1rem;
            border-radius: 18px;
        }

        .hero-title {
            font-size: 2rem;
        }

        .hero-subline {
            font-size: 0.96rem;
            max-width: 100%;
        }
    }
</style>
""", unsafe_allow_html=True)

model = load_model()


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


# --- SIDEBAR ---
with st.sidebar:
    st.markdown("## 🛡️ PhishGuard")
    st.caption("Phishing detection demo for email, SMS, and URL screening")

    st.divider()

    st.markdown("### Project Overview")
    st.markdown("""
    **Category:** Cybersecurity / Machine Learning  
    **Framework:** Streamlit  
    **Model:** Passive-Aggressive Classifier  
    **Dataset:** UCI SMS Spam Collection
    """)

    st.divider()

    st.markdown("### How to Use")
    st.markdown("""
    1. Select **Email**, **SMS**, or **URL Heuristics**  
    2. Enter the content you want to inspect  
    3. Review the risk result and explanation
    """)

    st.divider()

    st.markdown("### Analysis Notes")
    st.markdown("""
    - Email and SMS checks are model-based  
    - URL screening is rule-based in the current version  
    - Results should be treated as screening support, not final proof
    """)

    st.divider()

    st.markdown("### Developer")
    st.markdown("**Aryan Parth**")


# --- MAIN UI ---
st.markdown("""
<div class="hero-spacer"></div>
<div class="hero-card">
    <div class="hero-inner">
        <div class="hero-badge">Cybersecurity Portfolio Project</div>
        <div class="hero-title">PhishGuard: Phishing Detection System</div>
        <div class="hero-subline">
            Analyze suspicious email text, SMS content, and URLs through a cleaner phishing review interface
            for quick screening and clearer presentation.
        </div>
        <div class="hero-meta">
            <span class="hero-chip">Streamlit App</span>
            <span class="hero-chip">TF-IDF + Passive-Aggressive</span>
            <span class="hero-chip">Email • SMS • URL Review</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

tabs = st.tabs(["📧 Email Analysis", "💬 SMS Analysis", "🔗 URL Heuristics"])

for i, mode in enumerate(["email", "sms", "url"]):
    with tabs[i]:
        if mode == "email":
            st.markdown("### Input Text (Email)")
            st.caption("Paste email content to test the current phishing model.")
            user_data = st.text_area(
                "Input Text (Email)",
                height=220,
                placeholder="Paste email content to test the model...",
                label_visibility="collapsed"
            )

        elif mode == "sms":
            st.markdown("### Input Text (SMS)")
            st.caption("Enter SMS content for phishing or spam-like screening.")
            user_data = st.text_input(
                "Input Text (SMS)",
                placeholder="Enter SMS text...",
                label_visibility="collapsed"
            )

        else:
            st.markdown("### Input URL")
            st.caption("Enter a full URL to run the current heuristic link screening.")
            user_data = st.text_input(
                "Input URL",
                placeholder="https://example-site.com",
                label_visibility="collapsed"
            )

        analyze = st.button(f"Analyze {mode.upper()}", key=f"analyze_{mode}")

        if analyze:
            clean_input = normalize_text(user_data) if user_data else ""

            if not clean_input:
                st.warning("Please enter some content to analyze.")
                st.stop()

            with st.spinner("Model processing..."):
                try:
                    if mode in ["email", "sms"]:
                        risk, reason, trust_note = analyze_text(model, clean_input, mode, get_result_reason)
                    else:
                        if not is_valid_url(clean_input):
                            st.warning("Please enter a valid URL starting with http:// or https://")
                            st.stop()

                        risk, reason, trust_note = analyze_url(clean_input, get_result_reason)

                    st.markdown('<div class="result-box">', unsafe_allow_html=True)
                    st.markdown("### Analysis Result")
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
                    st.markdown('</div>', unsafe_allow_html=True)

                except Exception as e:
                    st.error("Something went wrong while analyzing the input.")
                    st.exception(e)
        else:
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.markdown("### Analysis Result")
            st.caption("The current result will appear here after analysis.")
            st.info("Run the analysis to view the risk gauge, verdict, and explanation.")
            st.markdown('</div>', unsafe_allow_html=True)


# --- FOOTER ---
st.divider()
st.markdown("""
### 📊 Methodology
This project utilizes a **TF-IDF (Term Frequency-Inverse Document Frequency)** vectorization method to convert text into numerical features, followed by a **Passive-Aggressive Classifier**. This specific algorithm was chosen for its high efficiency in binary text classification tasks.

**Note:** Email and SMS analysis are model-based. URL analysis currently uses rule-based screening in this Phase 2 version.
""")