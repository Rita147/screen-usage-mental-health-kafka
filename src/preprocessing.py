import pandas as pd
from sklearn.preprocessing import StandardScaler

RAW_PATH = "data/raw/screen_time_mental_health.csv"
OUT_PATH = "data/processed/screen_time_mental_health_clean.csv"

# Columns we want to scale (numerical continuous metrics)
NUM_COLS = [
    "daily_screen_time_hours",
    "phone_usage_hours",
    "laptop_usage_hours",
    "tablet_usage_hours",
    "tv_usage_hours",
    "social_media_hours",
    "work_related_hours",
    "entertainment_hours",
    "gaming_hours",
    "sleep_duration_hours",
    "physical_activity_hours_per_week",
    "caffeine_intake_mg_per_day",
    "mindfulness_minutes_per_day",
    "weekly_anxiety_score",
    "weekly_depression_score",
    "mood_rating",
    "stress_level",
    "mental_health_score"
]

# Categorical columns (will one-hot encode)
CAT_COLS = ["gender", "location_type", "uses_wellness_apps", "eats_healthy"]


def load_raw():
    return pd.read_csv(RAW_PATH)


def clean_df(df):
    # Fill numeric NaN with median
    df[NUM_COLS] = df[NUM_COLS].fillna(df[NUM_COLS].median())

    # Categorical → fill missing with mode
    for col in CAT_COLS:
        df[col] = df[col].fillna(df[col].mode()[0])

    return df


def encode_and_scale(df):
    # One-hot encode categorical
    df_enc = pd.get_dummies(df, columns=CAT_COLS, drop_first=True)

    # Standardize numerical columns
    scaler = StandardScaler()
    df_enc[NUM_COLS] = scaler.fit_transform(df_enc[NUM_COLS])

    return df_enc


def main():
    df = load_raw()
    df = clean_df(df)
    df = encode_and_scale(df)
    df.to_csv(OUT_PATH, index=False)

    print("Saved cleaned dataset to:", OUT_PATH)
    print("New shape:", df.shape)


if __name__ == "__main__":
    main()
