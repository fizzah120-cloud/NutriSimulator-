import streamlit as st
import random
import time
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

# -----------------------------
# FOOD DATABASE
# -----------------------------
foods = {
    # 🐔 Proteins (healthy core)
    "Chicken Breast 🐔": {"protein": 30, "carbs": 0, "fats": 5},
    "Boiled Eggs 🥚": {"protein": 12, "carbs": 1, "fats": 10},
    "Grilled Fish 🐟": {"protein": 28, "carbs": 0, "fats": 8},
    "Lentils (Daal) 🥣": {"protein": 18, "carbs": 30, "fats": 2},
    "Greek Yogurt 🥛": {"protein": 10, "carbs": 6, "fats": 4},

    # 🍚 Carbs (energy foods)
    "White Rice 🍚": {"protein": 4, "carbs": 45, "fats": 1},
    "Brown Rice 🌾": {"protein": 5, "carbs": 40, "fats": 2},
    "Whole Wheat Roti 🫓": {"protein": 6, "carbs": 30, "fats": 3},
    "Oats 🥣": {"protein": 8, "carbs": 27, "fats": 5},
    "Banana 🍌": {"protein": 1, "carbs": 27, "fats": 0},

    # 🥦 Vegetables (defense/health)
    "Broccoli 🥦": {"protein": 3, "carbs": 6, "fats": 0},
    "Spinach 🥬": {"protein": 3, "carbs": 4, "fats": 0},
    "Carrot 🥕": {"protein": 1, "carbs": 10, "fats": 0},
    "Cucumber 🥒": {"protein": 1, "carbs": 5, "fats": 0},

    # 🥑 Healthy Fats
    "Almonds 🌰": {"protein": 6, "carbs": 6, "fats": 14},
    "Walnuts 🥜": {"protein": 5, "carbs": 4, "fats": 18},
    "Avocado 🥑": {"protein": 3, "carbs": 12, "fats": 15},
    "Olive Oil 🫒": {"protein": 0, "carbs": 0, "fats": 14},

    # 🍔 Fast Food (risk items)
    "Burger 🍔": {"protein": 15, "carbs": 40, "fats": 22},
    "Fries 🍟": {"protein": 3, "carbs": 35, "fats": 18},
    "Pizza 🍕": {"protein": 12, "carbs": 35, "fats": 20},
    "Fried Chicken 🍗": {"protein": 20, "carbs": 10, "fats": 25},
    "Soda 🥤": {"protein": 0, "carbs": 38, "fats": 0},

    # 🍰 Sugary / Junk (high risk)
    "Chocolate Bar 🍫": {"protein": 3, "carbs": 30, "fats": 12},
    "Ice Cream 🍦": {"protein": 4, "carbs": 28, "fats": 14},
    "Donut 🍩": {"protein": 4, "carbs": 35, "fats": 18},

    # 🇵🇰 Pakistani Foods (real-life immersion)
    "Biryani 🍛": {"protein": 18, "carbs": 55, "fats": 20},
    "Nihari 🍲": {"protein": 22, "carbs": 10, "fats": 30},
    "Karahi 🍗": {"protein": 25, "carbs": 8, "fats": 25},
    "Paratha 🫓": {"protein": 5, "carbs": 30, "fats": 18},
    "Chai ☕": {"protein": 2, "carbs": 12, "fats": 5},

    # 🧬 Special / Rare Foods (game rewards)
    "Salmon 🐟": {"protein": 32, "carbs": 0, "fats": 12},
    "Quinoa 🌾": {"protein": 12, "carbs": 35, "fats": 6},
    "Chia Seeds ⚡": {"protein": 8, "carbs": 10, "fats": 20},
}

# -----------------------------
# PATIENT SYSTEM
# -----------------------------
patients = {
    "Fatigue Student 😴": {"protein": 20, "carbs": 40, "fats": 10},
    "Athlete 🏃‍♂️": {"protein": 50, "carbs": 60, "fats": 20},
    "Overweight ⚖️": {"protein": 30, "carbs": 30, "fats": 10},
    "Child Growth 👶": {"protein": 25, "carbs": 45, "fats": 15},
}

# -----------------------------
# LEVEL SYSTEM
# -----------------------------
def add_xp(points):
    st.session_state.xp += points
    if st.session_state.xp >= st.session_state.level * 100:
        st.session_state.level += 1
        st.success(f"🎉 LEVEL UP! You are now Level {st.session_state.level}")

# -----------------------------
# SIDEBAR PROFILE
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
st.write("Advanced medical nutrition simulation game")

# -----------------------------
# DAILY CHALLENGE MODE
# -----------------------------
st.subheader("⚡ Daily Challenge Mode")

if st.button("Start Random Patient Challenge"):
    patient = random.choice(list(patients.keys()))
    st.session_state.current_patient = patient
    st.info(f"New Patient: {patient}")

# -----------------------------
# PATIENT SELECTION
# -----------------------------
if "current_patient" not in st.session_state:
    st.session_state.current_patient = list(patients.keys())[0]

patient = st.selectbox("Select Patient:", list(patients.keys()), index=list(patients.keys()).index(st.session_state.current_patient))
target = patients[patient]

st.write(f"### 🧍 Condition Target: {patient}")
st.write(target)

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

st.subheader("🏆 Score")
st.metric("Nutrition Score", f"{int(score)}/100")
st.progress(score / 100)

# save history
st.session_state.score_history.append(score)

# -----------------------------
# COMBO SYSTEM
# -----------------------------
if score >= 80:
    st.session_state.streak += 1
    combo = st.session_state.streak * 1.5
    st.success(f"🔥 Combo x{combo}")
    add_xp(int(40 * combo))
else:
    st.session_state.streak = 0

# -----------------------------
# RANDOM EVENTS (GAME TWIST)
# -----------------------------
event = random.choice(["none", "vitamin_boost", "junk_crisis", "patient_recovery"])

if event == "vitamin_boost":
    st.info("🧪 Event: Vitamin Boost Day! Bonus XP x2")
    add_xp(20)

elif event == "junk_crisis":
    st.warning("⚠️ Event: Junk Food Crisis! Harder scoring this round")

elif event == "patient_recovery":
    st.success("💚 Patient naturally recovering! Bonus score added")
    score += 10

# -----------------------------
# FEEDBACK SYSTEM
# -----------------------------
st.subheader("🧠 AI Feedback")

if score >= 80:
    st.success("Excellent treatment! Patient recovering 🟢")
    st.balloons()
    add_xp(40)

elif score >= 50:
    st.warning("Good plan, but needs improvement 🟡")
    add_xp(20)

else:
    st.error("Critical condition 🔴")
    add_xp(5)

# -----------------------------
# NUTRITION CHARTS
# -----------------------------
st.subheader("📊 Nutrition Breakdown")

chart_data = pd.DataFrame({
    "Nutrients": ["Protein", "Carbs", "Fats"],
    "Amount": [protein, carbs, fats]
})

st.bar_chart(chart_data.set_index("Nutrients"))

# -----------------------------
# LEADERBOARD
# -----------------------------
st.subheader("🏆 Leaderboard")

name = st.text_input("Enter your name for leaderboard")

if st.button("Save Score"):
    if name:
        st.session_state.leaderboard[name] = score
        st.success("Score saved!")

if st.session_state.leaderboard:
    st.write(pd.DataFrame(
        list(st.session_state.leaderboard.items()),
        columns=["Player", "Score"]
    ).sort_values(by="Score", ascending=False))

# -----------------------------
# HISTORY
# -----------------------------
st.subheader("📈 Score History")
st.line_chart(st.session_state.score_history)
