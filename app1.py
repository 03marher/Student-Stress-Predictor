import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Page setup
st.set_page_config(
    page_title="Student Stress Predictor",
    page_icon="🧠",
    layout="centered"
)

# Custom styling
st.markdown("""
<style>
.main {
    background-color: #f7f9fc;
}
.stButton>button {
    width: 100%;
    border-radius: 12px;
    height: 3em;
    font-size: 16px;
}
.block-container {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# LOAD DATA + TRAIN MODEL
# -----------------------------
df = pd.read_excel("StudentStressFactors.xlsx")

# Rename columns to match model
df.columns = [
    "sleep_quality",
    "headaches",
    "academic_performance",
    "study_load",
    "extra_activities",
    "stress_level"
]

X = df[["sleep_quality", "headaches", "academic_performance", "study_load", "extra_activities"]]
y = df["stress_level"]

model = RandomForestClassifier()
model.fit(X, y)

# -----------------------------
# UI
# -----------------------------
st.title("🧠 Student Stress Predictor")
st.caption("Understand how your daily habits may impact your stress levels")

st.info("⚠️ This tool is for educational purposes only and is not a substitute for professional or clinical advice.")

st.markdown("---")

st.subheader("📋 Enter Your Information")

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        sleep_quality = st.slider("😴 Sleep Quality", 1, 5)
        headaches = st.slider("🤕 Headaches", 1, 5)
        academic_performance = st.slider("📚 Academic Performance", 1, 5)

    with col2:
        study_load = st.slider("📝 Study Load", 1, 5)
        extra_activities = st.slider("🎯 Extracurricular Activities", 1, 5)

st.markdown("---")

# -----------------------------
# PREDICTION
# -----------------------------
if st.button("🔍 Predict My Stress Level"):

    input_data = pd.DataFrame({
        "sleep_quality": [sleep_quality],
        "headaches": [headaches],
        "academic_performance": [academic_performance],
        "study_load": [study_load],
        "extra_activities": [extra_activities]
    })

    prediction = model.predict(input_data)[0]

    st.subheader("📊 Your Result")

    score = int(prediction) * 20

    st.write(f"### Stress Score: {score}/100")
    st.progress(score)
    st.caption("Low ←──────────────→ High")

    if score >= 80:
        st.caption("⚠️ Very high stress range")
    elif score >= 60:
        st.caption("Moderate to high stress")
    elif score >= 40:
        st.caption("Balanced range")
    else:
        st.caption("Low stress range")

    if prediction >= 4:
        st.error("🔴 High Stress Level")
    elif prediction == 3:
        st.warning("🟡 Moderate Stress Level")
    else:
        st.success("🟢 Low Stress Level")

    st.balloons()

# Footer
st.markdown("---")
st.caption("Built as a student project | Not intended for medical use")
