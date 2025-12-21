import json
from kafka import KafkaConsumer

TOPIC = "screen_activity"
BOOTSTRAP_SERVERS = "localhost:9092"

STRESS_THRESHOLD = 7          # tune based on dataset stats
SCREEN_TIME_THRESHOLD = 6     # hours/day, for example

def main():
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="screen-alerts-group",
    )

    for msg in consumer:
        e = msg.value
        stress = e.get("Stress Level", 0) or 0
        screen_time = e.get("Screen Time", 0) or 0

        if stress >= STRESS_THRESHOLD and screen_time >= SCREEN_TIME_THRESHOLD:
            print("[ALERT] High risk event:")
            print("   Age:", e.get("Age"),
                  "Screen Time:", screen_time,
                  "Stress:", stress,
                  "Anxiety:", e.get("Anxiety Score"),
                  "Depression:", e.get("Depression Score"))

if _name_ == "_main_":
    main()