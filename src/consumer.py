import json
import joblib
import pandas as pd
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

# =======================
# Kafka configuration
# =======================
KAFKA_TOPIC = "mental-health-stream"
KAFKA_SERVER = "localhost:9092"

# =======================
# Model configuration
# =======================
MODEL_PATH = "models/mental_health_model.pkl"
TARGET_COL = "mental_health_score"

# Columns that were NOT used during training
NON_FEATURE_COLS = [
    "user_id",
    "event_time"
]

# =======================
# Anomaly detection
# =======================
ANOMALY_THRESHOLD = 1.5


def main():
    print("Starting Prediction Consumer...")
    print("Loading trained model...")

    # Load model once
    model = joblib.load(MODEL_PATH)
    print("Model loaded successfully.")

    # Initialize Kafka consumer
    try:
        consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=[KAFKA_SERVER],
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            group_id="prediction-consumer-group",
            value_deserializer=lambda x: json.loads(x.decode("utf-8"))
        )
    except NoBrokersAvailable:
        print("Kafka broker not available. Is Docker running?")
        return

    try:
        for message in consumer:
            data = message.value

            # Metadata
            user_id = data.get("user_id", "unknown")
            actual_score = data.get(TARGET_COL, None)

            # Convert Kafka message to DataFrame
            df = pd.DataFrame([data])

            # Drop non-feature + target columns safely
            df_model = df.drop(
                columns=NON_FEATURE_COLS + [TARGET_COL],
                errors="ignore"
            )

            # Predict
            predicted_score = model.predict(df_model)[0]

            # Output + anomaly detection
            if actual_score is not None:
                error = abs(predicted_score - actual_score)

                alert = ""
                if error > ANOMALY_THRESHOLD:
                    alert = "  ANOMALY DETECTED"

                print(
                    f"User {user_id} | "
                    f"Actual: {actual_score:.2f} | "
                    f"Predicted: {predicted_score:.2f} | "
                    f"Error: {error:.2f}"
                    f"{alert}"
                )
            else:
                print(
                    f"User {user_id} | "
                    f"Predicted: {predicted_score:.2f}"
                )

    except KeyboardInterrupt:
        print("\nStopping prediction consumer...")
    finally:
        consumer.close()


if __name__ == "__main__":
    main()
