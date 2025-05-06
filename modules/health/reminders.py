import streamlit as st
import datetime

# 🔊 Function to play an online sound when a reminder is due
def play_alert_sound():
    """Plays an online alert sound using Streamlit's HTML audio player."""
    sound_url = "https://www.myinstants.com/media/sounds/tindeck_1.mp3"  # Online beep sound

    st.markdown(f"""
        <audio autoplay>
            <source src="{sound_url}" type="audio/mp3">
        </audio>
        """, unsafe_allow_html=True)

def reminders():
    """Manages medication, meal, and workout reminders in Streamlit."""

    st.subheader("🔔 Reminder System")

    # ─────────────────────────────────────────────────────────────────────────────
    # 📌 Initialize Session State for Reminders
    # ─────────────────────────────────────────────────────────────────────────────
    if "medication_list" not in st.session_state:
        st.session_state.medication_list = []
    
    if "meal_list" not in st.session_state:
        st.session_state.meal_list = []

    if "workout_list" not in st.session_state:
        st.session_state.workout_list = []

    # ─────────────────────────────────────────────────────────────────────────────
    # 📅 Reminder Selection
    # ─────────────────────────────────────────────────────────────────────────────
    reminder_type = st.radio("Select Reminder Type:", ["Medication", "Meal", "Workout"], horizontal=True)

    # Common input fields
    reminder_name = st.text_input(f"Enter {reminder_type} Name")
    reminder_time = st.time_input(f"Set {reminder_type} Reminder Time", datetime.time(9, 0))  # Default 9:00 AM

    if st.button(f"➕ Add {reminder_type} Reminder"):
        if reminder_name.strip():
            reminder_entry = {"name": reminder_name, "time": reminder_time}

            if reminder_type == "Medication":
                st.session_state.medication_list.append(reminder_entry)
                st.success(f"✅ Medication Reminder set for **{reminder_name}** at **{reminder_time.strftime('%I:%M %p')}**")
            
            elif reminder_type == "Meal":
                st.session_state.meal_list.append(reminder_entry)
                st.success(f"✅ Meal Reminder set for **{reminder_name}** at **{reminder_time.strftime('%I:%M %p')}**")
            
            elif reminder_type == "Workout":
                st.session_state.workout_list.append(reminder_entry)
                st.success(f"✅ Workout Reminder set for **{reminder_name}** at **{reminder_time.strftime('%I:%M %p')}**")
        else:
            st.warning(f"⚠️ Please enter a {reminder_type} name.")

    # ─────────────────────────────────────────────────────────────────────────────
    # 📝 Display and Manage Reminders
    # ─────────────────────────────────────────────────────────────────────────────
    st.write("### 📋 Your Reminders")

    def display_reminders(title, reminder_list_key):
        """Displays a list of reminders and allows deletion."""
        if st.session_state[reminder_list_key]:
            st.write(f"#### {title}")
            for idx, reminder in enumerate(st.session_state[reminder_list_key]):
                st.write(f"**{reminder['name']}** - {reminder['time'].strftime('%I:%M %p')}")
                if st.button(f"❌ Remove {reminder['name']}", key=f"{reminder_list_key}_{idx}"):
                    st.session_state[reminder_list_key].pop(idx)
                    st.rerun()  # Refresh UI after deletion
        else:
            st.info(f"No {title.lower()} reminders set.")

    display_reminders("💊 Medication Reminders", "medication_list")
    display_reminders("🍽️ Meal Reminders", "meal_list")
    display_reminders("🏋️ Workout Reminders", "workout_list")

    # ─────────────────────────────────────────────────────────────────────────────
    # ⏰ Check for Due Reminders (Real-Time Alerts)
    # ─────────────────────────────────────────────────────────────────────────────
    current_time = datetime.datetime.now().time()

    for category, reminder_list_key in [
        ("Medication", "medication_list"),
        ("Meal", "meal_list"),
        ("Workout", "workout_list")
    ]:
        for reminder in st.session_state[reminder_list_key]:
            if reminder["time"].hour == current_time.hour and reminder["time"].minute == current_time.minute:
                st.warning(f"🔔 Time for your {category.lower()}: **{reminder['name']}**!")
                play_alert_sound()  # 🎵 Play online alert sound when reminder is due
