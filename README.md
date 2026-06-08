# SentiFlow AI - Twitter Sentiment Analysis Dashboard

## Overview

SentiFlow AI is an AI-powered Twitter Sentiment Analysis Dashboard that uses Natural Language Processing (NLP) and Machine Learning to classify tweets as Positive or Negative in real time.

The project leverages TF-IDF Vectorization, Logistic Regression, Streamlit, and Plotly to provide an interactive analytics dashboard with sentiment insights and visualizations.

---

## Features

* Real-Time Tweet Sentiment Analysis
* NLP Text Preprocessing
* TF-IDF Feature Extraction
* Logistic Regression Classification
* Interactive Streamlit Dashboard
* Modern SaaS-Inspired UI
* Sentiment Analytics Visualization
* Prediction History Tracking
* Business Insights Dashboard

---

## Tech Stack

* Python
* Pandas
* NumPy
* Scikit-Learn
* Streamlit
* Plotly
* Joblib

---

## Machine Learning Pipeline

Tweet Input
↓
Text Cleaning
↓
TF-IDF Vectorization
↓
Logistic Regression Model
↓
Sentiment Prediction

---

## Dataset

Dataset Used: Sentiment140

The original dataset contains 1.6 million tweets labeled as:

* Positive (4)
* Negative (0)

Note: The dataset is not included in this repository due to GitHub file size limitations.

Dataset Source:
https://www.kaggle.com/datasets/kazanova/sentiment140

---

## Model Performance

* Training Samples: 50,000 Tweets
* Algorithm: Logistic Regression
* Feature Engineering: TF-IDF
* Accuracy: ~76.9%

---

## Project Structure

twitter-sentiment-analysis/

├── app/
│ └── app.py

├── models/
│ ├── sentiment_model.pkl
│ └── tfidf_vectorizer.pkl

├── train.py

├── requirements.txt

├── README.md

└── .gitignore

---

## Screenshots

### Dashboard Home

(Add Screenshot Here)

### Positive Sentiment Prediction

(Add Screenshot Here)

### Negative Sentiment Prediction

(Add Screenshot Here)

---

## Author

Ankit Kumar Jha

GitHub:
https://github.com/ankitjha2621

---

## Future Improvements

* Multi-Class Sentiment Analysis
* LLM-Based Sentiment Classification
* Real-Time Twitter API Integration
* Emotion Detection
* Explainable AI Features
