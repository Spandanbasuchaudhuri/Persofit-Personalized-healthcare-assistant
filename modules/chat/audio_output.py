# File: modules/chat/audio_output.py

import streamlit as st
import os
import tempfile
import base64
import asyncio
from edge_tts import Communicate

def get_available_voices():
    """Returns a list of available Microsoft Edge TTS voices."""
    return [
        "en-US-JennyNeural",
        "en-US-GuyNeural",
        "en-GB-SoniaNeural",
        "en-GB-RyanNeural",
        "en-IN-NeerjaNeural",
        "en-IN-PrabhatNeural",
        "en-AU-NatashaNeural",
        "en-AU-WilliamNeural"
    ]

def text_to_speech(text):
    """
    Converts AI-generated text to speech using Edge TTS and plays it in Streamlit.
    Make sure 'enable_audio' is toggled in session_state or skip if not needed.
    """
    if not text.strip():
        return  # Skip if text is empty

    try:
        selected_voice = st.session_state.get("selected_voice", "en-US-JennyNeural")
        temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        temp_path = temp_audio.name
        temp_audio.close()

        # Run Edge TTS asynchronously
        asyncio.run(Communicate(text, voice=selected_voice, rate="+0%").save(temp_path))

        # Convert to base64 and play in an HTML audio tag
        with open(temp_path, "rb") as audio_file:
            audio_bytes = audio_file.read()
            audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")

        audio_html = f"""
        <audio autoplay>
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)

        os.remove(temp_path)

    except Exception as e:
        st.error(f"Error in text-to-speech: {e}")
