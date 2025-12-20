import pandas as pd
from datetime import datetime, timedelta

IN_PATH = "data/processed/screen_time_mental_health_clean.csv"
OUT_PATH = "data/processed/screen_time_mental_health_stream.csv"

def main():
    # Load cleaned data
    df = pd.read_csv(IN_PATH)

    # Starting timestamp for the stream
    start = datetime(2024, 1, 1, 8, 0, 0)

    # Spread events every 3 minutes (you can change this)
    step = timedelta(minutes=3)

    # Create event_time column
    df["event_time"] = [start + i * step for i in range(len(df))]

    # Save streaming-ready file
    df.to_csv(OUT_PATH, index=False)

    print("Created stream-ready dataset at:", OUT_PATH)
    print("Rows:", len(df))


if __name__ == "__main__":
    main()
