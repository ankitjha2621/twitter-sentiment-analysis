import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

columns = [
    "sentiment",
    "id",
    "date",
    "query",
    "user",
    "text"
]

print("Loading Dataset...")

df = pd.read_csv(
    "data/training.1600000.processed.noemoticon.csv",
    encoding="latin-1",
    names=columns
)

print("Dataset Loaded!")

df = df.sample(50000, random_state=42)

def clean_text(text):

    text = text.lower()

    text = re.sub(r"@\w+", "", text)

    text = re.sub(r"http\S+", "", text)

    text = re.sub(r"[^a-zA-Z\s]", "", text)

    return text

print("Cleaning Tweets...")

df["clean_text"] = df["text"].apply(clean_text)

print("Applying TF-IDF...")

vectorizer = TfidfVectorizer(max_features=5000)

X = vectorizer.fit_transform(df["clean_text"])

print("TF-IDF Matrix Shape:")
print(X.shape)
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Convert labels
y = df["sentiment"]

# Train-Test Split
print("Splitting Dataset...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("Training Model...")

model = LogisticRegression(max_iter=1000)

model.fit(X_train, y_train)

print("Model Trained!")

# Predictions
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print(f"Accuracy: {accuracy:.4f}")
joblib.dump(model, "models/sentiment_model.pkl")
joblib.dump(vectorizer, "models/tfidf_vectorizer.pkl")

print("Model Saved Successfully!")