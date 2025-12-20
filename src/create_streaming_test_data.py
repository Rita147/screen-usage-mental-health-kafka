import pandas as pd
from sklearn.model_selection import train_test_split

# paths
DATA_PATH = "data/processed/screen_time_mental_health_clean.csv"
OUT_PATH = "data/processed/streaming_test_data.csv"

TARGET_COL = "mental_health_score"

def main():
    print("Loading dataset...")
    df = pd.read_csv(DATA_PATH)

    print("Full dataset shape:", df.shape)

    # Split ONLY to isolate test data
    _, df_test = train_test_split(
        df,
        test_size=0.2,
        random_state=42
    )

    print("Streaming test data shape:", df_test.shape)

    # Save test data
    df_test.to_csv(OUT_PATH, index=False)

    print(f"Saved streaming test data to: {OUT_PATH}")


if __name__ == "__main__":
    main()
