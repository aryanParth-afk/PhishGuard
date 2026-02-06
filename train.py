import pandas as pd
import joblib
import urllib.request
import zipfile
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.pipeline import Pipeline

# 1. LOAD DATASET (UCI Repository - Standard for academic projects)
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00228/smsspamcollection.zip"
urllib.request.urlretrieve(url, "data.zip")
with zipfile.ZipFile("data.zip", 'r') as z:
    df = pd.read_csv(z.open("SMSSpamCollection"), sep='\t', names=['label', 'text'])
df['label'] = df['label'].map({'spam': 1, 'ham': 0})

# 2. RESEARCH-GRADE PIPELINE
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english', ngram_range=(1, 2), max_features=5000)),
    ('pa', PassiveAggressiveClassifier(max_iter=1000, random_state=42))
])

print("🎓 Training PhishGuard Academic Model...")
pipeline.fit(df['text'], df['label'])

# 3. SAVE
joblib.dump(pipeline, 'phishguard_model.pkl')
print("✅ Project Artifacts Generated: phishguard_model.pkl")
