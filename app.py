import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="Nutritionist Simulator PRO", layout="centered")

# -----------------------------
# SESSION STATE INIT
# -----------------------------
if "xp" not in st.session_state:
    st.session_state.xp = 0
    st.session_state.level = 1
    st.session_state.streak = 0
    st.session_state.score_history = []
    st.session_state.leaderboard = {}
    st.session_state.current_patient = None

# -----------------------------
# FOOD DATABASE
# -----------------------------
foods = {
    "Chicken Breast 🐔": {"protein": 30, "carbs": 0, "fats": 5},
    "Boiled Eggs 🥚": {"protein": 12, "carbs": 1, "fats": 10},
    "Grilled Fish 🐟": {"protein": 28, "carbs": 0, "fats": 8},
    "Lentils (Daal) 🥣": {"protein": 18, "carbs": 30, "fats": 2},
    "Greek Yogurt 🥛": {"protein": 10, "carbs": 6, "fats": 4},
    "White Rice 🍚": {"protein": 4, "carbs": 45, "fats": 1},
    "Brown Rice 🌾": {"protein": 5, "carbs": 40, "fats": 2},
    "Whole Wheat Roti 🫓": {"protein": 6, "carbs": 30, "fats": 3},
    "Oats 🥣": {"protein": 8, "carbs": 27, "fats": 5},
    "Banana 🍌": {"protein": 1, "carbs": 27, "fats": 0},
    "Broccoli 🥦": {"protein": 3, "carbs": 6, "fats": 0},
    "Spinach 🥬": {"protein": 3, "carbs": 4, "fats": 0},
    "Carrot 🥕": {"protein": 1, "carbs": 10, "fats": 0},
    "Cucumber 🥒": {"protein": 1, "carbs": 5, "fats": 0},
    "Almonds 🌰": {"protein": 6, "carbs": 6, "fats": 14},
    "Burger 🍔": {"protein": 15, "carbs": 40, "fats": 22},
    "Fries 🍟": {"protein": 3, "carbs": 35, "fats": 18},
    "Pizza 🍕": {"protein": 12, "carbs": 35, "fats": 20},
    "Fried Chicken 🍗": {"protein": 20, "carbs": 10, "fats": 25},
    "Soda 🥤": {"protein": 0, "carbs": 38, "fats": 0},
    "Chocolate Bar 🍫": {"protein": 3, "carbs": 30, "fats": 12},
    "Ice Cream 🍦": {"protein": 4, "carbs": 28, "fats": 14},
    "Biryani 🍛": {"protein": 18, "carbs": 55, "fats": 20},
    "Nihari 🍲": {"protein": 22, "carbs": 10, "fats": 30},
    "Paratha 🫓": {"protein": 5, "carbs": 30, "fats": 18},
}

# -----------------------------
# 15+ PATIENT DATABASE
# -----------------------------
patients = {
    "Fatigue Student 😴": {"protein": 20, "carbs": 40, "fats": 10},
    "Athlete 🏃‍♂️": {"protein": 50, "carbs": 60, "fats": 20},
    "Overweight ⚖️": {"protein": 30, "carbs": 30, "fats": 10},
    "Child Growth 👶": {"protein": 25, "carbs": 45, "fats": 15},
    "Diabetic Patient 🩸": {"protein": 30, "carbs": 25, "fats": 15},
    "Heart Patient ❤️": {"protein": 35, "carbs": 20, "fats": 10},
    "Bodybuilder 💪": {"protein": 70, "carbs": 50, "fats": 25},
    "Underweight Patient 🦴": {"protein": 40, "carbs": 60, "fats": 20},
    "Office Worker 🪑": {"protein": 25, "carbs": 35, "fats": 15},
    "Teen Growth 📈": {"protein": 30, "carbs": 55, "fats": 18},
    "Elderly Patient 👴": {"protein": 20, "carbs": 30, "fats": 12},
    "Fat Loss Client 🔥": {"protein": 45, "carbs": 25, "fats": 10},
    "Pregnant Patient 🤰": {"protein": 50, "carbs": 55, "fats": 25},
    "Athletic Runner 🏃": {"protein": 55, "carbs": 65, "fats": 18},
    "Recovery Patient 🏥": {"protein": 40, "carbs": 40, "fats": 20},
}

# -----------------------------
# LEVEL SYSTEM
# -----------------------------
def add_xp(points):
    st.session_state.xp += points
    if st.session_state.xp >= st.session_state.level * 100:
        st.session_state.level += 1
        st.success(f"🎉 LEVEL UP! Now Level {st.session_state.level}")

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("🧑‍⚕️ Doctor Profile")
st.sidebar.write(f"⭐ Level: {st.session_state.level}")
st.sidebar.write(f"🔥 XP: {st.session_state.xp}")
st.sidebar.write(f"🏆 Streak: {st.session_state.streak}")
st.sidebar.progress((st.session_state.xp % 100) / 100)

# -----------------------------
# TITLE
# -----------------------------
st.title("🧑‍⚕️ Nutritionist Simulator PRO")
st.write("Hospital-level nutrition simulation system")

# -----------------------------
# RANDOM PATIENT MODE
# -----------------------------
if st.button("🎲 Generate Random Patient"):
    st.session_state.current_patient = random.choice(list(patients.keys()))

# -----------------------------
# SELECT PATIENT
# -----------------------------
if not st.session_state.current_patient:
    st.session_state.current_patient = list(patients.keys())[0]

patient = st.selectbox(
    "Select Patient",
    list(patients.keys()),
    index=list(patients.keys()).index(st.session_state.current_patient)
)

st.session_state.current_patient = patient
target = patients[patient]

# -----------------------------
# PATIENT FILE
# -----------------------------
st.subheader("📁 Patient File")

st.write(f"Name: {patient}")
st.write("Target Nutrition:")
st.json(target)

# -----------------------------
# FOOD SELECTION
# -----------------------------
selected = st.multiselect("Select Foods:", list(foods.keys()))

protein = sum(foods[f]["protein"] for f in selected)
carbs = sum(foods[f]["carbs"] for f in selected)
fats = sum(foods[f]["fats"] for f in selected)

# -----------------------------
# SCORE CALCULATION
# -----------------------------
diff = abs(target["protein"] - protein) + abs(target["carbs"] - carbs) + abs(target["fats"] - fats)
score = max(0, 100 - diff)

st.subheader("🏆 Nutrition Score")
st.metric("Score", f"{int(score)}/100")
st.progress(score / 100)

st.session_state.score_history.append(score)

# -----------------------------
# DIAGNOSIS
# -----------------------------
st.subheader("🧠 Medical Diagnosis")

if score >= 80:
    st.success("✔ Patient improving well")
    st.balloons()
    add_xp(40)
    st.session_state.streak += 1

elif score >= 50:
    st.warning("⚠ Stable but needs improvement")
    add_xp(20)
    st.session_state.streak = 0

else:
    st.error("🚨 Critical imbalance")
    add_xp(5)
    st.session_state.streak = 0

# -----------------------------
# NUTRITION REPORT
# -----------------------------
st.subheader("📄 Nutrition Report")

report = {
    "Patient": patient,
    "Protein Intake": protein,
    "Carbs Intake": carbs,
    "Fats Intake": fats,
    "Target Protein": target["protein"],
    "Target Carbs": target["carbs"],
    "Target Fats": target["fats"],
    "Score": int(score)
}

st.json(report)

# -----------------------------
# CHARTS
# -----------------------------
st.subheader("📊 Macro Breakdown")

df = pd.DataFrame({
    "Nutrients": ["Protein", "Carbs", "Fats"],
    "Amount": [protein, carbs, fats]
})

st.bar_chart(df.set_index("Nutrients"))

# -----------------------------
# LEADERBOARD
# -----------------------------
st.subheader("🏆 Leaderboard")

name = st.text_input("Enter Doctor Name")

if st.button("Save Score"):
    if name:
        st.session_state.leaderboard[name] = score

if st.session_state.leaderboard:
    st.dataframe(
        pd.DataFrame(
            list(st.session_state.leaderboard.items()),
            columns=["Doctor", "Score"]
        ).sort_values("Score", ascending=False)
    )

# -----------------------------
# HISTORY
# -----------------------------
st.subheader("📈 Score History")
st.line_chart(st.session_state.score_history)
