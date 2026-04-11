import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import math

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
.gauge-container {
    text-align: center;
    margin-top: 10px;
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
y = df["stress_level"]

model = RandomForestClassifier()
model.fit(X, y)

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
# GAUGE (REAL HALF CIRCLE)
# -----------------------------
def gauge_html(score):
    rotation = (score / 100) * 180 - 90

    x = 150 + 100 * math.cos(math.radians(rotation))
    y = 150 - 100 * math.sin(math.radians(rotation))

    return f"""
    <div class="gauge-container">
        <svg width="300" height="180">

            <!-- Background arc -->
            <path d="M50 150 A100 100 0 0 1 250 150"
                  fill="none" stroke="#eee" stroke-width="20"/>

            <!-- Low -->
            <path d="M50 150 A100 100 0 0 1 150 50"
                  fill="none" stroke="#4CAF50" stroke-width="20"/>

            <!-- Moderate -->
            <path d="M150 50 A100 100 0 0 1 210 90"
                  fill="none" stroke="#FFC107" stroke-width="20"/>

            <!-- High -->
            <path d="M210 90 A100 100 0 0 1 250 150"
                  fill="none" stroke="#F44336" stroke-width="20"/>

            <!-- Needle -->
            <line x1="150" y1="150"
                  x2="{x}" y2="{y}"
                  stroke="#333" stroke-width="4"/>

            <!-- Center dot -->
            <circle cx="150" cy="150" r="6" fill="#333"/>

        </svg>

        <div style="font-size:22px; font-weight:bold; margin-top:5px;">
            {score}/100
        </div>
    </div>
    """

# -----------------------------
# HEADER
# -----------------------------
st.title("🧠 Student Stress Predictor")
st.caption("Estimate your stress level based on your habits")

st.info("⚠️ Educational tool only. Not medical advice.")

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
# SESSION STATE (IMPORTANT FIX)
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

    prediction = model.predict(input_data)[0]
    score = int(prediction) * 20

    if score >= 80:
        level = "High"
    elif score >= 60:
        level = "Moderate"
    else:
        level = "Low"

    st.session_state.result = (score, level)

# -----------------------------
# DISPLAY RESULT (FIXED)
# -----------------------------
if st.session_state.result:

    score, level = st.session_state.result

    st.subheader("📊 Your Result")

    st.markdown(gauge_html(score), unsafe_allow_html=True)

    if level == "High":
        st.error("🔴 High Stress Level")
    elif level == "Moderate":
        st.warning("🟡 Moderate Stress Level")
    else:
        st.success("🟢 Low Stress Level")

    st.markdown("### 💡 Recommendations")

    tips = get_recommendations(level)

    for tip in tips:
        st.write(f"• {tip}")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("Built as a student project | Not medical advice")
