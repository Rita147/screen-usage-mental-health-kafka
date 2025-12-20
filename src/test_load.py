import pandas as pd

df = pd.read_csv("data/raw/screen_time_mental_health.csv")

print("Rows, Cols:", df.shape)
print(df.head())
