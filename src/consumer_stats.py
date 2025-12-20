import json
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

KAFKA_TOPIC = "mental-health-stream"
KAFKA_SERVER = "localhost:9092"

def main():
    print("Starting Stats Consumer...")

    try:
        consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=[KAFKA_SERVER],
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            group_id="stats-consumer-group",
            value_deserializer=lambda x: json.loads(x.decode("utf-8"))
        )
    except NoBrokersAvailable:
        print("Kafka not available. Did you run docker-compose up?")
        return

    count = 0
    total_screen_time = 0.0
    total_stress = 0.0
    total_mental_health = 0.0

    try:
        for message in consumer:
            data = message.value
            count += 1

            # defensive access (streaming mindset)
            total_screen_time += float(data.get("daily_screen_time_hours", 0))
            total_stress += float(data.get("stress_level", 0))
            total_mental_health += float(data.get("mental_health_score", 0))

            if count % 10 == 0:
                print("---- Running Statistics ----")
                print(f"Records processed: {count}")
                print(f"Avg screen time: {total_screen_time / count:.2f}")
                print(f"Avg stress level: {total_stress / count:.2f}")
                print(f"Avg mental health score: {total_mental_health / count:.2f}")
                print("----------------------------")

    except KeyboardInterrupt:
        print("Stopping stats consumer...")
    finally:
        consumer.close()

if __name__ == "__main__":
    main()
