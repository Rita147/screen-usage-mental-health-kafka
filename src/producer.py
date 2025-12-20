import pandas as pd
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
import json
import time

# stream data csv
DATA_PATH = "data/processed/streaming_test_data_stream.csv"

KAFKA_SERVER = "localhost:9092"
KAFKA_TOPIC = "mental-health-stream"
SIM_DELAY_SEC = 0.5 

def main():
    print("Starting Kafka Producer...")

    # init producer
    try:
        producer = KafkaProducer(
            bootstrap_servers=[KAFKA_SERVER],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
    except NoBrokersAvailable:
        print(f"Error: Kafka broker at {KAFKA_SERVER} not found.")
        print("Please make sure Kafka is running (e.g., with 'docker-compose up -d').")
        return
    except Exception as e:
        print(f"An error occurred while connecting to Kafka: {e}")
        return

    # load data
    try:
        df = pd.read_csv(DATA_PATH)
        print(f"Loaded {len(df)} records from {DATA_PATH}")
    except FileNotFoundError:
        print(f"Error: Data file not found at {DATA_PATH}")
        print("Please check the relative path from where you are running the script.")
        return

    # iterate and send msgs
    print(f"Streaming data to Kafka topic: '{KAFKA_TOPIC}'...")

    for index, row in df.iterrows():
        message = row.to_dict()
        # send
        producer.send(KAFKA_TOPIC, value=message)
        print(f"Sent: user_id {message.get('user_id')} at {message.get('event_time')}")
        time.sleep(SIM_DELAY_SEC)

    producer.flush()
    producer.close()
    print("--- Stream simulation finished. All messages sent. ---")

if __name__ == "__main__":
    main()