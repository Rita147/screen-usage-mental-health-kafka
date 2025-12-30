# Dynamic Correlation between Screen Usage and Mental Well-Being: A Kafka-Based Approach

A data mining project analyzing dynamic correlations between screen time and mental health indicators using Apache Kafka’s real-time stream processing capabilities.

This project implements a real-time data mining pipeline to analyze the relationship between screen usage patterns and mental well-being. It uses **Apache Kafka** for data streaming, a **Random Forest** model for anomaly detection, and **Streamlit** for a live monitoring dashboard.

## 📋 Prerequisites

Before running the project, ensure you have the following installed:
* **Docker Desktop** (for running Kafka & Zookeeper)
* **Python 3.8+**

## ⚙️ Installation

1.  **Clone the repository** (if applicable) or navigate to the project root:
    ```bash
    cd screen-usage-mental-health-kafka
    ```

2.  **Install Python Dependencies:**
    Create a `requirements.txt` file (or use the one provided) and install the necessary libraries:
    ```bash
    pip install kafka-python pandas scikit-learn joblib streamlit numpy
    ```

    > **Note:** If you encounter a `numpy.dtype size changed` error, force a reinstall of the compatible versions:
    > `pip install --upgrade --force-reinstall numpy scikit-learn joblib`

## 🚀 How to Run the Pipeline

You will need to open **three separate terminal windows** to run the full pipeline. Ensure all terminals are open in the project root directory.

### Step 1: Start the Kafka Infrastructure (Terminal 1)
Start the Zookeeper and Kafka containers using Docker Compose.

```bash
docker-compose up -d
```

Wait a few seconds for the containers to fully initialize.

### Step 2: Start the Consumer (Terminal 1)
The consumer loads the trained model and listens for incoming data to make predictions and detect anomalies.

```bash
python src/consumer.py
```
You should see a message indicating the model is loaded and it is waiting for messages.

### Step 3: Launch the Dashboard (Terminal 2)
Start the Streamlit interface to visualize the real-time data and alerts.

```bash
python -m streamlit run src/dashboard.py
```
This will automatically open the dashboard in your default web browser (usually at http://localhost:8501).

### Step 4: Start the Producer (Terminal 3)
Finally, start the producer to begin simulating the stream of user data.

```bash
python src/producer.py
```
You will now see data appearing in the Consumer terminal and the Dashboard will update in real-time.

## 🛑 Stopping the Project
To stop the services, press Ctrl+C in the python terminals. To shut down the Docker containers, run:

```bash
docker-compose down
```
## 📂 Project Structure
src/producer.py: Simulates real-time data ingestion by streaming user records.

src/consumer.py: Consumes data, runs the Random Forest model, and detects anomalies.

src/dashboard.py: Streamlit web app for visualization.

src/train_model.py: Script used to train the Random Forest Regressor on historical data.

docker-compose.yml: Configuration for Kafka and Zookeeper services.

## 👥 Authors
Özge Bülbül

Rita Sulaiman


