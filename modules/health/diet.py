# File: modules/health/diet.py

import streamlit as st
import ollama
from modules.chat.audio_output import text_to_speech

def recommend_diet():
    """AI-powered diet plan with chunked streaming output + auto TTS toggle."""
    st.subheader("🥗 AI-Powered Diet Plan")

    # Local auto voice toggle
    if "diet_auto_voice" not in st.session_state:
        st.session_state["diet_auto_voice"] = False

    st.session_state["diet_auto_voice"] = st.checkbox(
        "Auto Voice Output (Diet)",
        value=st.session_state["diet_auto_voice"]
    )

    # User inputs
    goal_options = ["Weight Loss", "Muscle Gain", "Healthy Eating", "Others"]
    goal = st.radio("What is your diet goal?", goal_options)
    if goal == "Others":
        goal = st.text_input("Specify your diet goal:")

    diet_options = ["None", "Vegetarian", "Vegan", "Keto", "Low-Carb", "Others"]
    diet_type = st.radio("Any specific diet?", diet_options)
    if diet_type == "Others":
        diet_type = st.text_input("Specify your diet type:")

    allergies = st.text_area("Any food allergies?")
    foods_to_avoid = st.text_area("Foods to avoid?")

    if st.button("Generate Diet Plan"):
        st.write("### 🍽️ Your AI-Generated Diet Plan")

        prompt = f"""
        You are a professional nutritionist. Generate a structured diet plan:
        - Goal: {goal}
        - Diet Preference: {diet_type}
        - Allergies: {allergies}
        - Foods to Avoid: {foods_to_avoid}
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

            # Auto TTS if checked
            if st.session_state["diet_auto_voice"]:
                text_to_speech(full_response)

        except Exception as e:
            st.error("❌ Ollama API error.")
            st.code(str(e), language="bash")
