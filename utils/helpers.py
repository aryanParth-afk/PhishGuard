import re
from urllib.parse import urlparse


def normalize_text(text):
    return re.sub(r"\s+", " ", text.strip())


def is_valid_url(text):
    try:
        parsed = urlparse(text.strip())
        return parsed.scheme in ("http", "https") and bool(parsed.netloc)
    except Exception:
        return False


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