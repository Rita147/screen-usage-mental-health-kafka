import time
import json
import joblib
import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

KAFKA_TOPIC = "mental-health-stream"
KAFKA_SERVER = "localhost:9092"
MODEL_PATH = "models/mental_health_model.pkl"
TARGET_COL = "mental_health_score"
NON_FEATURE_COLS = ["user_id", "event_time"]

st.set_page_config(page_title="Mental Health AI Monitor", layout="wide", page_icon="🧠")

st.markdown("""
<style>
    div[data-testid="stMetric"] {
        background-color: #FCE4EC;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #E91E63;
    }
    div[data-testid="stMetric"] * {
        color: #880E4F !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("🧠 Real-Time Mental Health Monitoring System")
st.markdown("**Rita Sulaiman & Özge Bülbül** | *Live AI Analysis of Screen Habits*")

st.sidebar.header("⚙️ Controls")
ANOMALY_THRESHOLD = st.sidebar.slider("Anomaly Threshold", 0.5, 3.0, 1.5)
PAUSE = st.sidebar.checkbox("⏸️ Pause Stream")

st.sidebar.divider()
st.sidebar.subheader("📊 Session Stats")
stat_anomalies = st.sidebar.empty()
stat_mae = st.sidebar.empty()

def get_status_label(val):
    if val > 1.0: return "High ⬆️"
    if val < -1.0: return "Low ⬇️"
    return "Avg ⏺️"

col1, col2, col3, col4 = st.columns(4)
metric_user = col1.empty()
metric_actual = col2.empty()
metric_pred = col3.empty()
metric_status = col4.empty()

st.divider()

st.subheader("💗 Prediction Accuracy Stream (Actual vs AI)")
chart_line = st.empty()

st.divider()

c1, c2 = st.columns(2)
with c1:
    st.subheader("🧠 Detailed Mental State")
    chart_mental = st.empty()
with c2:
    st.subheader("📱 Screen Usage Breakdown")
    chart_screen = st.empty()

st.divider()

st.subheader("❤️ User Wellness Vitals (Relative Levels)")
w1, w2, w3, w4 = st.columns(4)
metric_sleep = w1.empty()
metric_activity = w2.empty()
metric_caffeine = w3.empty()
metric_mood = w4.empty()

st.divider()

st.subheader("Incoming Data Log")
table_placeholder = st.empty()

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

def init_consumer():
    try:
        return KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=[KAFKA_SERVER],
            value_deserializer=lambda x: json.loads(x.decode("utf-8")),
            auto_offset_reset="latest",
            group_id="dashboard-monitor-group-final-v3"
        )
    except NoBrokersAvailable:
        st.error("❌ Kafka not found. Is Docker running?")
        st.stop()

def main():
    model = load_model()
    consumer = init_consumer()
    
    history = pd.DataFrame(columns=["timestamp", "actual", "predicted", "error", "user_id"])
    total_anomalies = 0
    total_error = 0
    count = 0

    for message in consumer:
        if PAUSE:
            time.sleep(1)
            continue

        data = message.value
        
        # 1MODEL PREDICTION
        user_id = data.get("user_id", "Unknown")
        event_time = data.get("event_time", "")
        actual_score = data.get(TARGET_COL, 0)
        
        df_row = pd.DataFrame([data])
        X_input = df_row.drop(columns=NON_FEATURE_COLS + [TARGET_COL], errors="ignore")
        
        try:
            predicted_score = model.predict(X_input)[0]
        except Exception:
            continue
            
        error = abs(predicted_score - actual_score)
        is_anomaly = error > ANOMALY_THRESHOLD
        
        count += 1
        total_error += error
        if is_anomaly: total_anomalies += 1
            
        stat_anomalies.metric("Total Anomalies", total_anomalies)
        stat_mae.metric("Model MAE", f"{total_error/count:.3f}")

        # HISTORY
        new_row = {"timestamp": event_time, "actual": actual_score, "predicted": predicted_score, "error": error, "user_id": user_id}
        history = pd.concat([history, pd.DataFrame([new_row])], ignore_index=True)
        if len(history) > 60: history = history.iloc[-60:]
            
        
        # Top Metricss
        metric_user.metric("User ID", user_id)
        metric_actual.metric("Actual Score", f"{actual_score:.2f}")
        metric_pred.metric("AI Prediction", f"{predicted_score:.2f}", delta=f"{actual_score - predicted_score:.2f}")
        
        if is_anomaly: metric_status.error(f"⚠️ ANOMALY")
        else: metric_status.success("✅ Normal")

        # MAIN CHART
        chart_data = history[["timestamp", "actual", "predicted"]].melt("timestamp", var_name="Type", value_name="Score")
        line_chart = alt.Chart(chart_data).mark_line(point=True, strokeWidth=3).encode(
            x=alt.X("timestamp", axis=alt.Axis(labels=False), title="Time"),
            y=alt.Y("Score", scale=alt.Scale(domain=[-2.5, 3.5])),
            # Dark Raspberry for Actual, Bright Pink for AI
            color=alt.Color("Type", scale=alt.Scale(range=['#880E4F', '#FF4081']), legend=alt.Legend(title="Legend")),
            tooltip=["timestamp", "Score", "Type"]
        ).properties(height=300)
        chart_line.altair_chart(line_chart, use_container_width=True)

        # Mental state chart
        mental_cols = ["stress_level", "weekly_anxiety_score", "weekly_depression_score"]
        mental_data = {k: data.get(k, 0) for k in mental_cols}
        mental_df = pd.DataFrame(list(mental_data.items()), columns=["Metric", "Level"])
        
        c_mental = alt.Chart(mental_df).mark_bar().encode(
            x=alt.X("Metric", axis=alt.Axis(labelAngle=0)),
            y=alt.Y("Level"),
            color=alt.Color("Metric", scale=alt.Scale(range=['#F8BBD0', '#F06292', '#880E4F'])),
            tooltip=["Metric", "Level"]
        ).properties(height=250)
        chart_mental.altair_chart(c_mental, use_container_width=True)

        # Screen usage chart
        usage_cols = ["social_media_hours", "work_related_hours", "gaming_hours", "entertainment_hours"]
        usage_data = {k: data.get(k, 0) for k in usage_cols}
        usage_df = pd.DataFrame(list(usage_data.items()), columns=["Activity", "Hours"])
        
        c_usage = alt.Chart(usage_df).mark_bar(color="#F06292").encode(
            x=alt.X("Activity", axis=alt.Axis(labelAngle=-45)),
            y="Hours", tooltip=["Activity", "Hours"]
        ).properties(height=250)
        chart_screen.altair_chart(c_usage, use_container_width=True)

        # Wellness Vitals
        val_sleep = data.get("sleep_duration_hours", 0)
        val_phys = data.get("physical_activity_hours_per_week", 0)
        val_caff = data.get("caffeine_intake_mg_per_day", 0)
        val_mood = data.get("mood_rating", 0)

        metric_sleep.metric("Sleep Duration", get_status_label(val_sleep), f"{val_sleep:.2f} (Z)")
        metric_activity.metric("Phys. Activity", get_status_label(val_phys), f"{val_phys:.2f} (Z)")
        metric_caffeine.metric("Caffeine", get_status_label(val_caff), f"{val_caff:.2f} (Z)")
        metric_mood.metric("Mood Rating", get_status_label(val_mood), f"{val_mood:.2f} (Z)")

        table_placeholder.dataframe(history.tail(5)[["timestamp", "user_id", "actual", "predicted", "error"]])
        
        time.sleep(0.05) 

if __name__ == "__main__":
    main()