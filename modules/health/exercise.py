# File: modules/health/exercise.py

import streamlit as st
import ollama
from modules.chat.audio_output import text_to_speech

def recommend_exercise():
    """AI-powered exercise plan with streaming + local auto TTS toggle."""
    st.subheader("🏋️ Personalized Exercise Plan")

    if "exercise_auto_voice" not in st.session_state:
        st.session_state["exercise_auto_voice"] = False

    st.session_state["exercise_auto_voice"] = st.checkbox(
        "Auto Voice Output (Exercise)",
        value=st.session_state["exercise_auto_voice"]
    )

    goal_options = ["Weight Loss", "Muscle Gain", "Endurance", "General Fitness", "Others"]
    goal = st.radio("What is your fitness goal?", goal_options)
    if goal == "Others":
        goal = st.text_input("Specify your goal:")

    level_options = ["Beginner", "Intermediate", "Advanced", "Others"]
    experience = st.radio("What is your experience level?", level_options)
    if experience == "Others":
        experience = st.text_input("Specify your level:")

    time_available = st.slider("Daily exercise time (minutes):", 10, 120, 30)
    equipment = st.radio("Access to gym equipment?", ["Yes", "No"])
    injury = st.text_area("Any injuries to consider?")

    if st.button("Generate Exercise Plan"):
        st.write("### 📋 Your AI-Generated Exercise Plan")

        prompt = f"""
        You are a professional fitness trainer. Generate a structured plan:
        - Goal: {goal}
        - Experience Level: {experience}
        - Available Time: {time_available} minutes
        - Equipment: {equipment}
        - Injuries: {injury}
        """

        full_response = ""
        placeholder = st.empty()

        try:
            response = ollama.chat(
                model="llama3",
                messages=[{"role": "user", "content": prompt}],
                stream=True
            )
            for chunk in response:
                full_response += chunk["message"]["content"]
                placeholder.markdown(full_response)

            # Speak automatically if checkbox is ON
            if st.session_state["exercise_auto_voice"]:
                text_to_speech(full_response)

        except Exception as e:
            st.error("❌ Ollama API error.")
            st.code(str(e), language="bash")