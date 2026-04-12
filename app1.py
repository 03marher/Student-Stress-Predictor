import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import plotly.graph_objects as go

# -----------------------------
# PAGE SETUP
# -----------------------------
st.set_page_config(
    page_title="Student Stress Predictor",
    page_icon="🧠",
    layout="centered"
)

# -----------------------------
# STYLING
# -----------------------------
st.markdown("""
<style>
.block-container {
    max-width: 800px;
    padding-top: 2rem;
}
.stButton>button {
    width: 100%;
    border-radius: 12px;
    height: 3em;
    font-size: 16px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# LOAD DATA + MODEL
# -----------------------------
df = pd.read_excel("StudentStressFactors.xlsx")

df.columns = [
    "sleep_quality",
    "headaches",
    "academic_performance",
    "study_load",
    "extra_activities",
    "stress_level"
]

X = df[[
    "sleep_quality",
    "headaches",
    "academic_performance",
    "study_load",
    "extra_activities"
]]
def categorize_stress(x):
    if x >= 4:
        return "High"
    elif x == 3:
        return "Moderate"
    else:
        return "Low"

y = df["stress_level"].apply(categorize_stress)

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Scale data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train model
model = LogisticRegression(max_iter=1000)
model.fit(X_train_scaled, y_train)

# Accuracy (optional but useful)
accuracy = model.score(X_test_scaled, y_test)
st.caption(f"Model accuracy: {round(accuracy * 100, 1)}%")

# -----------------------------
# RECOMMENDATIONS
# -----------------------------
def get_recommendations(level):
    if level == "Low":
        return [
            "Maintain your current balance and healthy habits.",
            "Keep a consistent sleep schedule.",
            "Stay proactive with your workload."
        ]
    elif level == "Moderate":
        return [
            "Break tasks into smaller chunks.",
            "Plan your week ahead to avoid overload.",
            "Aim for better sleep consistency."
        ]
    else:
        return [
            "Reduce workload if possible.",
            "Reach out to academic or counseling support.",
            "Prioritize rest and recovery."
        ]

# -----------------------------
# PLOTLY GAUGE
# -----------------------------
def plotly_gauge(score):

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': "Stress Score"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "#2b7cff"},
            'steps': [
                {'range': [0, 40], 'color': "#4CAF50"},
                {'range': [40, 70], 'color': "#FFC107"},
                {'range': [70, 100], 'color': "#F44336"}
            ]
        }
    ))

    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# HEADER
# -----------------------------
st.title("🧠 Student Stress Predictor")
st.caption("Estimate your stress level based on your habits")

st.info("⚠️ This is an educational tool and not medical advice.")

st.divider()

# -----------------------------
# INPUTS
# -----------------------------
st.subheader("📋 Enter Your Information")

st.markdown("Use a scale from **1 (Very Low/Poor)** to **5 (Very High/Excellent)**.")

col1, col2 = st.columns(2)

with col1:
    sleep_quality = st.slider("😴 Sleep Quality (1 = Poor, 5 = Excellent)", 1, 5)
    headaches = st.slider("🤕 Headache Frequency (1 = Rare, 5 = Frequent)", 1, 5)
    academic_performance = st.slider("📚 Academic Performance (1 = Low, 5 = High)", 1, 5)

with col2:
    study_load = st.slider("📝 Study Load (1 = Light, 5 = Heavy)", 1, 5)
    extra_activities = st.slider("🎯 Extracurricular Involvement (1 = Low, 5 = High)", 1, 5)

st.divider()

# -----------------------------
# SESSION STATE (fix for results)
# -----------------------------
if "result" not in st.session_state:
    st.session_state.result = None

# -----------------------------
# BUTTON
# -----------------------------
if st.button("🔍 Predict Stress Level"):

    input_data = pd.DataFrame({
        "sleep_quality": [sleep_quality],
        "headaches": [headaches],
        "academic_performance": [academic_performance],
        "study_load": [study_load],
        "extra_activities": [extra_activities]
    })

    input_scaled = scaler.transform(input_data)
    prediction = model.predict(input_scaled)[0]

# Convert prediction into score
if prediction == "High":
    score = 85
elif prediction == "Moderate":
    score = 60
else:
    score = 35

level = prediction

    st.session_state.result = (score, level)

# -----------------------------
# DISPLAY RESULTS
# -----------------------------
if st.session_state.result:

    score, level = st.session_state.result

    st.subheader("📊 Your Result")

    # Gauge (FIXED)
    plotly_gauge(score)

    # Status message
    if level == "High":
        st.error("🔴 High Stress Level")
    elif level == "Moderate":
        st.warning("🟡 Moderate Stress Level")
    else:
        st.success("🟢 Low Stress Level")

    # Recommendations (FIXED)
    st.markdown("### 💡 Recommendations")

    tips = get_recommendations(level)

    for tip in tips:
        st.write(f"• {tip}")

st.markdown("### 📊 Model Info")
st.write(f"Accuracy: {round(accuracy * 100, 1)}%")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("Built as a student project | Not medical advice")
