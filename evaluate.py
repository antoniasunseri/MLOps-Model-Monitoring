import requests
import json

API_URL = "http://localhost:8000/predict"

with open("C:/Users/anton/OneDrive - University of Denver/Autumn Quarter 2025/COMP 4450 - ML Ops/Assignment 5/MLOps-Model-Monitoring/test.json") as f:
    test_data = json.load(f)

correct = 0
for item in test_data:
    response = requests.post(API_URL, json={"text": item["text"], "true_sentiment": item["true_label"]})
    pred = response.json()["predicted_sentiment"]
    if pred == item["true_label"]:
        correct += 1

accuracy = correct / len(test_data) * 100
print(f"Evaluation Accuracy: {accuracy:.2f}%")
