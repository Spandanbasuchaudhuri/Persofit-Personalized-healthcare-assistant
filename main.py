import streamlit as st

# ✅ Ensure you're on a recent Streamlit (≥1.18) for st.rerun()
st.set_page_config(page_title="Multimodal AI Assistant", layout="wide")

# Updated imports based on subfolders
from modules.chat.ai_response import generate_response
from modules.health.exercise import recommend_exercise
from modules.health.diet import recommend_diet
from modules.health.reminders import reminders
from modules.chat.audio_output import get_available_voices

st.title("🤖 Multimodal AI Assistant")

# ─────────────────────────────────────────────────────────────────────────────
# 🔊 Sidebar Settings
# ─────────────────────────────────────────────────────────────────────────────
st.sidebar.header("Settings")

# 1) Audio Toggle
enable_audio = st.sidebar.checkbox("🔊 Enable AI Voice Output", value=False)
st.session_state["enable_audio"] = enable_audio

# 2) Voice Selection
if "selected_voice" not in st.session_state:
    st.session_state["selected_voice"] = "en-US-JennyNeural"

voices = get_available_voices()
current_voice = st.session_state["selected_voice"]
default_index = voices.index(current_voice) if current_voice in voices else 0

st.sidebar.selectbox(
    "Select Voice:",
    voices,
    index=default_index,
    key="selected_voice"
)

# ─────────────────────────────────────────────────────────────────────────────
# 🏥 Health Assistant Feature Selection
# ─────────────────────────────────────────────────────────────────────────────
st.sidebar.header("🏥 Health Assistant")
health_feature = st.sidebar.radio(
    "Select a Feature:",
    ["AI Chat", "Exercise Plan", "Diet Plan", "Reminders"]
)

if health_feature == "AI Chat":
    generate_response()
elif health_feature == "Exercise Plan":
    recommend_exercise()
elif health_feature == "Diet Plan":
    recommend_diet()
elif health_feature == "Reminders":
    reminders()