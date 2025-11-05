# MLOps Model Monitoring

This project demonstrates a **multi-container MLOps monitoring system**:

1. **FastAPI Prediction Service**: Serves sentiment predictions for movie reviews.  
2. **Streamlit Monitoring Dashboard**: Visualizes data drift, target drift, model accuracy, and alerts based on logged predictions.  
3. **Evaluation Script**: Automatically evaluates the model using a test dataset.  
4. **Dockerized Containers**: Reproducible deployment for both API and monitoring dashboard.

---

### **Prerequisites:**
- **Docker Installation**  
  **See** Docker Desktop: [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)  
- **Python 3.8+**

---

### **How to Run**

1. Open Command Prompt

2. **Clone the repository**:

```bash
git clone https://github.com/antoniasunseri/MLOps-Model-Monitoring.git
cd MLOps-Model-Monitoring
```

3. **Run FastAPI Prediction Service**
   - Navigate to API folder:
     ```bash
     cd api
     ```
   - Install dependencies (if not using Docker):
     ```bash
     python -m pip install fastapi uvicorn joblib
     ```
   - Start API server:
     ```bash
     python -m uvicorn main:app --reload
     ```
   - API runs at `http://127.0.0.1:8000`  
   - Test endpoint: `http://127.0.0.1:8000/docs`
   - Example CURL request:
     ```bash
     curl -X POST "http://127.0.0.1:8000/predict" \
      -H "Content-Type: application/json" \
      -d "{\"text\": \"I loved this movie!\", \"true_sentiment\": \"positive\"}"
      ```

4. **Run Evaluation Script**
   - From project root:
     ```bash
     python evaluate.py
     ```
   - Sends requests from `test.json` to the API
   - Prints final **accuracy**
   - Logs saved to `logs/prediction_logs.json`

5. **Run Streamlit Monitoring Dashboard**
   - Navigate to monitoring folder:
     ```bash
     cd monitoring
     python -m streamlit run app.py
     ```
   - Access dashboard at [http://localhost:8501](http://localhost:8501)
   - Features:
     - Data Drift (sentence lengths)
     - Target Drift (predicted vs true sentiment)
     - Accuracy & Alerts if < 80%

---

### **How to Run Using Docker**

1. Build Docker images:
   ```bash
   docker build -t sentiment-api ./api
   docker build -t monitoring-dashboard ./monitoring
    ```
2. Use Makefile:

Build images:
```bash
make build
```
Run containers:
```bash
make run
```
Clean images and volumes:
```bash
make clean
```

### **Tips & Troubleshooting**
1. Verify Docker installation
2. Check running containers
3. Ensure ports 8000 (API) and 8501 (Streamlit) are free
4. Make sure FastAPI server is running before executing evaluate.py or starting Streamlit dashboard



