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
# GAUGE
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

st.info(
    "ℹ️ For best results, answer honestly based on your typical week.\n"
    "If something does not apply to you, select 1 (lowest value)."
)

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        "<div style='font-weight:600;'>Rating of the student’s sleep quality (1–5). 1 = Very poor, 5 = Excellent.</div>",
        unsafe_allow_html=True
    )
    sleep_quality = st.slider("😴 Sleep Quality", 1, 5)

    st.markdown(
        "<div style='font-weight:600;'>Number of times the student experiences headaches per week. 1 = Rare, 5 = Very frequent.</div>",
        unsafe_allow_html=True
    )
    headaches = st.slider("🤕 Headache Frequency", 1, 5)

    st.markdown(
        "<div style='font-weight:600;'>Self-assessed academic performance on a 1–5 scale. 1 = Low, 5 = High.</div>",
        unsafe_allow_html=True
    )
    academic_performance = st.slider("📚 Academic Performance", 1, 5)

with col2:
    st.markdown(
        "<div style='font-weight:600;'>Perceived heaviness of the student’s study workload (1–5). 1 = Light, 5 = Very heavy.</div>",
        unsafe_allow_html=True
    )
    study_load = st.slider("📝 Study Load", 1, 5)

    st.markdown(
        "<div style='font-weight:600;'>Number of times the student participates in extracurricular activities per week. 1 = Low involvement, 5 = Very active.</div>",
        unsafe_allow_html=True
    )
    extra_activities = st.slider("🎯 Extracurricular Activities", 1, 5)


# -----------------------------
# SESSION STATE
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
# DISPLAY RESULTS
# -----------------------------
if st.session_state.result:

    score, level = st.session_state.result

    st.subheader("📊 Your Result")

    plotly_gauge(score)

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
