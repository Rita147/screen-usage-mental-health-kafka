import pandas as pd
from datetime import datetime, timedelta

IN_PATH = "data/processed/streaming_test_data.csv"
OUT_PATH = "data/processed/streaming_test_data_stream.csv"

def main():
    df = pd.read_csv(IN_PATH)

    start = datetime(2024, 1, 1, 8, 0, 0)
    step = timedelta(minutes=3)

    df["event_time"] = [start + i * step for i in range(len(df))]

    df.to_csv(OUT_PATH, index=False)

    print("Created streaming test data with timestamps:")
    print(OUT_PATH)
    print("Rows:", len(df))

if __name__ == "__main__":
    main()
