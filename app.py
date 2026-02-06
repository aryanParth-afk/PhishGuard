import streamlit as st
import joblib
import plotly.graph_objects as go
import re
import time

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

# --- GAUGE ---
def draw_gauge(score):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number", value = score,
        title = {'text': "Confidence Score", 'font': {'size': 18, 'color': '#00d4ff'}},
        gauge = {
            'axis': {'range': [0, 100], 'tickcolor': "#00d4ff"},
            'bar': {'color': "#00d4ff"},
            'steps': [
                {'range': [0, 50], 'color': 'rgba(0, 255, 0, 0.1)'},
                {'range': [50, 100], 'color': 'rgba(255, 0, 0, 0.1)'}
            ]
        }
    ))
    fig.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)', font={'color': "#ffffff"})
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
                user_data = st.text_area("Input Text (Email)", height=200, placeholder="Paste email content to test the model...")
            elif mode == "sms":
                user_data = st.text_input("Input Text (SMS)", placeholder="Enter SMS text...")
            else:
                user_data = st.text_input("Input URL", placeholder="https://example-site.com")
            
            analyze = st.button(f"Analyze {mode.upper()}")

        with col2:
            if analyze and user_data:
                with st.spinner("Model processing..."):
                    if mode in ["email", "sms"]:
                        score_raw = model.decision_function([user_data])[0]
                        risk = min(max((score_raw + 1) / 2 * 100, 0), 100)
                    else:
                        # Academic Heuristic Logic
                        risk = 10
                        if "https" not in user_data: risk += 30
                        if len(user_data) > 60: risk += 20
                        if any(x in user_data.lower() for x in ['bit.ly', 'verify', 'update', 'login']): risk += 40
                    
                    st.plotly_chart(draw_gauge(risk), use_container_width=True)
                    
                    if risk > 70:
                        st.error("Result: Potential Malicious Intent")
                    elif risk > 30:
                        st.warning("Result: Suspicious Activity Detected")
                    else:
                        st.success("Result: Likely Benign / Safe")

# --- FOOTER ---
st.divider()
st.markdown("""
### 📊 Methodology
This project utilizes a **TF-IDF (Term Frequency-Inverse Document Frequency)** vectorization method to convert text into numerical features, followed by a **Passive-Aggressive Classifier**. This specific algorithm was chosen for its high efficiency in binary text classification tasks.
""")
