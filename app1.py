import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Page setup
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
.gauge-wrap {
    text-align: center;
    margin-top: 10px;
}
.gauge-arc {
    width: 260px;
    height: 130px;
    margin: 0 auto;
    position: relative;
    overflow: hidden;
}
.arc {
    position: absolute;
    width: 260px;
    height: 260px;
    border-radius: 50%;
    border: 20px solid transparent;
    top: 0;
    left: 0;
}
.low { border-top-color: #4CAF50; transform: rotate(210deg); }
.mid { border-top-color: #FFC107; transform: rotate(180deg); }
.high { border-top-color: #F44336; transform: rotate(150deg); }
.center {
    position: absolute;
    width: 180px;
    height: 180px;
    background: white;
    border-radius: 50%;
    left: 40px;
    top: 40px;
}
.needle {
    position: absolute;
    bottom: 10px;
    left: 50%;
    width: 5px;
    height: 80px;
    background: #333;
    transform-origin: bottom;
    transform: rotate(45deg);
}
.score-text {
    font-size: 1.8rem;
    font-weight: bold;
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

X = df[["sleep_quality", "headaches", "academic_performance", "study_load", "extra_activities"]]
y = df["stress_level"]

model = RandomForestClassifier()
model.fit(X, y)

# -----------------------------
# HEADER
# -----------------------------
st.title("🧠 Student Stress Predictor")
st.caption("Estimate your stress level based on your habits")

st.info("⚠️ This is an educational tool and not medical advice.")

st.divider()

# -----------------------------
# INPUTS (IMPROVED DESCRIPTIONS)
# -----------------------------
st.subheader("📋 Enter Your Information")

st.markdown("Use a scale from **1 (Very Low/Poor)** to **5 (Very High/Excellent)** based on your experience.")

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
# GAUGE FUNCTION
# -----------------------------
def gauge_html(score):
    rotation = int((score / 100) * 180 - 90)

    return f"""
    <div class="gauge-wrap">
        <div class="gauge-arc">
            <div class="arc low"></div>
            <div class="arc mid"></div>
            <div class="arc high"></div>
            <div class="center"></div>
            <div class="needle" style="transform: rotate({rotation}deg);"></div>
        </div>
        <div class="score-text">{score}/100</div>
    </div>
    """

# -----------------------------
# PREDICTION
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

    st.subheader("📊 Your Result")

    st.markdown(gauge_html(score), unsafe_allow_html=True)

    if score >= 80:
        st.error("🔴 High Stress Level")
    elif score >= 60:
        st.warning("🟡 Moderate Stress Level")
    else:
        st.success("🟢 Low Stress Level")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("Built as a student project | Not medical advice")
