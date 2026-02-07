# PhishGuard: Phishing Detection System 🛡️

PhishGuard is an end-to-end Machine Learning application designed to identify malicious communications. It provides a multi-layered defense analysis for Emails, SMS, and URLs using a high-performance Passive-Aggressive Classifier.

## 🚀 Live Demo
https://phishguard-pyuqhxgtkew9xefue6xbnb.streamlit.app/

## ✨ Key Features
- **📧 Email Analysis:** Scans full email body text for phishing indicators.
- **💬 SMS Analysis:** Quick detection of "smishing" (SMS phishing) attempts.
- **🔗 URL Heuristics:** Instant risk assessment of links based on security patterns and redirection keywords.
- **📊 Real-time Visualization:** Dynamic Gauge charts reflecting the model's confidence scores.

## 🛠️ Technical Methodology

### Machine Learning Pipeline
- **Vectorization:** TF-IDF (Term Frequency-Inverse Document Frequency) with a range of (1, 2) n-grams to capture both single keywords and suspicious phrases.
- **Algorithm:** **Passive-Aggressive Classifier**. This model was chosen for its efficiency in high-dimensional text classification and its ability to handle large-scale datasets with low latency.
- **Dataset:** Trained on the UCI SMS Spam Collection, a gold-standard dataset for communication security research.

### Why Passive-Aggressive?
Unlike traditional models, the Passive-Aggressive algorithm is ideal for security:
1. **Passive:** If the prediction is correct, the model remains unchanged.
2. **Aggressive:** If the prediction is wrong, it makes massive updates to correct its weights immediately.
This makes it highly adaptive to the evolving nature of phishing attacks.

## 📦 Installation and Functioning

1. **Install Dependencies:**

    in bash / terminal->
    pip install -r requirements.txt

2. **Run train.py file:** (optional , only if phishguard_model.pkl file not present)

     in bash/terminal->
     python train.py

3.  **Run the app:**

     in bash/terminal->
     streamlit run app.py   
   

 
