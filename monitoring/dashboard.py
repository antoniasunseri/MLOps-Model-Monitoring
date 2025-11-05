import streamlit as st
import pandas as pd
import json
import os
import matplotlib.pyplot as plt

LOG_FILE = "/logs/prediction_logs.json"
DATA_FILE = "C:/Users/anton/OneDrive - University of Denver/Autumn Quarter 2025/COMP 4450 - ML Ops/Assignment 5/MLOps-Model-Monitoring/monitoring/data/IMDB Dataset.csv"

st.title("Sentiment Model Monitoring Dashboard")

# Read logs
if os.path.exists(LOG_FILE):
    logs = [json.loads(line) for line in open(LOG_FILE)]
    df_logs = pd.DataFrame(logs)
else:
    st.warning("No logs available yet.")
    df_logs = pd.DataFrame()

# Read original dataset
df_data = pd.read_csv(DATA_FILE)

# Data Drift Analysis: Sentence length
if not df_logs.empty:
    df_logs["text_len"] = df_logs["request_text"].apply(len)
    df_data["text_len"] = df_data["review"].apply(len)

    st.subheader("Data Drift: Sentence Length")
    plt.hist(df_data["text_len"], bins=20, alpha=0.5, label="Training")
    plt.hist(df_logs["text_len"], bins=20, alpha=0.5, label="Live Requests")
    plt.legend()
    st.pyplot(plt)

# Target Drift Analysis
if not df_logs.empty:
    st.subheader("Target Drift: Predicted vs True Sentiment")
    pred_counts = df_logs["predicted_sentiment"].value_counts()
    true_counts = df_logs["true_sentiment"].value_counts()
    df_compare = pd.DataFrame({"Predicted": pred_counts, "True": true_counts}).fillna(0)
    st.bar_chart(df_compare)

# Accuracy Calculation
if not df_logs.empty and df_logs["true_sentiment"].notnull().any():
    correct = (df_logs["predicted_sentiment"] == df_logs["true_sentiment"]).sum()
    total = df_logs["true_sentiment"].notnull().sum()
    accuracy = correct / total * 100
    st.metric("Accuracy (from feedback)", f"{accuracy:.2f}%")

    if accuracy < 80:
        st.error("Accuracy has dropped below 80%! Alert!")
