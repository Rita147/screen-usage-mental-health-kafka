import json
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

# config
KAFKA_TOPIC = "mental-health-stream"
KAFKA_SERVER = "localhost:9092"

def main():
    print(f"Starting Consumer...")
    print(f"Connecting to Kafka at {KAFKA_SERVER}...")

    try:
        # init consumer
        consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=[KAFKA_SERVER],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='my-simple-consumer-group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        print(f"Connected! Waiting for messages on topic: '{KAFKA_TOPIC}'")
    except NoBrokersAvailable:
        print(f"Error: Could not connect to Kafka at {KAFKA_SERVER}.")
        print("   Make sure Docker is running with: 'docker-compose up -d'")
        return

    try:
        for message in consumer:
            data = message.value
            
            user = data.get('user_id', 'Unknown')
            time = data.get('event_time', 'Unknown')
            print(f"Received: User {user} at {time}")

    except KeyboardInterrupt:
        print("\nStopping consumer...")
    finally:
        consumer.close()

if __name__ == "__main__":
    main()