import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Student Stress Predictor",
    page_icon="🧠",
    layout="wide",
)

# -----------------------------
# LOAD DATA + TRAIN MODEL
# -----------------------------
df = pd.read_excel("StudentStressFactors.xlsx")

# Rename columns to clean names
df.columns = [
    "sleep_quality",
    "headaches",
    "academic_performance",
    "study_load",
    "extra_activities",
    "stress_level"
]

# ⚠️ If this errors, we will fix column names
X = df[["sleep_quality", "headaches", "academic_performance", "study_load", "extra_activities"]]
y = df["stress_level"]

model = RandomForestClassifier()
model.fit(X, y)

# -----------------------------
# REAL PREDICTION FUNCTION
# -----------------------------
def mock_predict_stress(credit_hours, work_hours, sleep_hours, study_hours, perceived_stress):

    input_data = pd.DataFrame({
        "sleep_quality": [sleep_hours],
        "headaches": [perceived_stress],
        "academic_performance": [3],  # placeholder
        "study_load": [study_hours],
        "extra_activities": [work_hours]
    })

    prediction = model.predict(input_data)[0]

    if prediction >= 4:
        return "High", 8.5
    elif prediction == 3:
        return "Moderate", 5.5
    else:
        return "Low", 3.0


# -----------------------------
# RECOMMENDATIONS
# -----------------------------
def get_recommendations(level):
    recommendations = {
        "Low": [
            "Keep a consistent sleep schedule and maintain healthy routines.",
            "Continue balancing classes, work, and breaks throughout the week.",
            "Check in with yourself regularly so stress does not gradually build up.",
        ],
        "Moderate": [
            "Break study sessions into smaller blocks with short breaks in between.",
            "Reduce overload where possible by planning your week ahead of time.",
            "Aim for 7–8 hours of sleep and protect time for rest.",
        ],
        "High": [
            "Consider reducing work or extracurricular load if possible.",
            "Reach out to academic support or campus counseling services for help.",
            "Prioritize recovery habits such as rest, hydration, and structured study planning.",
        ],
    }
    return recommendations[level]


# -----------------------------
# GAUGE UI
# -----------------------------
def gauge_html(level, score):
    level_color = {
        "Low": "#2e8b57",
        "Moderate": "#d88b1d",
        "High": "#c94b4b",
    }[level]

    left = 18
    if level == "Moderate":
        left = 50
    elif level == "High":
        left = 82

    return f"""
    <div class="gauge-wrap">
        <div class="gauge-arc">
            <div class="arc-segment low"></div>
            <div class="arc-segment moderate"></div>
            <div class="arc-segment high"></div>
            <div class="gauge-center"></div>
            <div class="needle" style="left: {left}%;"></div>
        </div>
        <div class="gauge-labels">
            <span>Low</span>
            <span>High</span>
        </div>
        <div class="stress-score" style="color: {level_color};">{level} Stress</div>
        <div class="stress-subtext">Predicted score: {score:.1f} / 10</div>
    </div>
    """


# -----------------------------
# STYLE (UNCHANGED)
# -----------------------------
st.markdown("""<style>
/* keep all your existing CSS exactly the same */
</style>""", unsafe_allow_html=True)

# -----------------------------
# TOP BAR
# -----------------------------
st.markdown("""
<div class="topbar">
    <div class="brand">🧠 Student Stress Predictor</div>
    <div class="nav">
        <span>Home</span>
        <span>About</span>
        <span>Contact</span>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# HERO
# -----------------------------
st.markdown("""
<div class="hero">
    <h1>Student Stress Predictor</h1>
    <p>Enter your current academic and lifestyle details to estimate your predicted stress level and receive supportive tips.</p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# SESSION STATE
# -----------------------------
if "predicted_level" not in st.session_state:
    st.session_state.predicted_level = "Moderate"
    st.session_state.predicted_score = 5.9

# -----------------------------
# LAYOUT
# -----------------------------
left_col, middle_col, right_col = st.columns([1.05, 1.15, 0.95], gap="large")

# -----------------------------
# LEFT: INPUTS
# -----------------------------
with left_col:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    credit_hours = st.number_input("Credit Hours", 0, 24, 15)
    work_hours = st.number_input("Work Hours Per Week", 0, 80, 10)
    sleep_hours = st.slider("Sleep Hours", 0.0, 12.0, 7.0)
    study_hours = st.number_input("Study Hours", 0, 80, 12)
    extracurricular_hours = st.number_input("Extracurricular Hours", 0, 40, 5)
    perceived_stress = st.slider("Stress Self-Assessment", 1, 10, 5)

    if st.button("Estimate Stress Level"):
        level, score = mock_predict_stress(
            credit_hours,
            work_hours,
            sleep_hours,
            study_hours,
            perceived_stress,
        )
        st.session_state.predicted_level = level
        st.session_state.predicted_score = score

    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# MIDDLE: RESULT
# -----------------------------
with middle_col:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown(
        gauge_html(st.session_state.predicted_level, st.session_state.predicted_score),
        unsafe_allow_html=True,
    )

    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# RIGHT: TIPS
# -----------------------------
with right_col:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    tips = get_recommendations(st.session_state.predicted_level)
    for tip in tips:
        st.write("•", tip)

    st.caption("Disclaimer: Not medical advice.")

    st.markdown('</div>', unsafe_allow_html=True)
