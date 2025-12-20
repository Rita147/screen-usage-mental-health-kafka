import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os

# paths
DATA_PATH = "data/processed/screen_time_mental_health_clean.csv"
MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "mental_health_model.pkl")

TARGET_COL = "mental_health_score"

# 🔴 CHANGE 1: columns to EXCLUDE from training
NON_FEATURE_COLS = [
    "user_id"  # identifier, not a feature
]


def main():
    print("Loading dataset...")
    df = pd.read_csv(DATA_PATH)

    print("Dataset shape:", df.shape)

    # 🔴 CHANGE 2: drop non-feature columns
    df_model = df.drop(columns=NON_FEATURE_COLS)

    # split features / target
    X = df_model.drop(columns=[TARGET_COL])
    y = df_model[TARGET_COL]

    # train / test split (80 / 20)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("Training samples:", X_train.shape[0])
    print("Testing samples:", X_test.shape[0])
    print("Number of features:", X_train.shape[1])

    # model
    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    )

    print("Training model...")
    model.fit(X_train, y_train)

    # evaluation
    print("Evaluating model...")
    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    r2 = r2_score(y_test, y_pred)

    print("----- Model Performance -----")
    print(f"MAE  : {mae:.3f}")
    print(f"RMSE : {rmse:.3f}")
    print(f"R²   : {r2:.3f}")
    print("-----------------------------")

    # save model
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    print(f"Model saved to: {MODEL_PATH}")


if __name__ == "__main__":
    main()
