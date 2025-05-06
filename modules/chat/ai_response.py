# File: modules/chat/ai_response.py

import streamlit as st
import ollama
from modules.chat.audio_output import text_to_speech

def generate_response():
    """
    Dark-themed AI chat with:
      - Local 'Auto Voice Output' checkbox
      - Streams chunk by chunk from Ollama
      - If checkbox is ON, TTS automatically plays the final AI message
      - "Clear Chat" button to reset conversation
    """

    st.subheader("💬 AI Chat Assistant")

    # 1) Dark Mode CSS
    chat_css = """
    <style>
        body {
            background-color: #000000;
            color: white;
        }
        .message-container {
            width: 100%;
            display: flex;
            margin-bottom: 12px;
        }
        .user-container {
            justify-content: flex-end;
        }
        .ai-container {
            justify-content: flex-start;
        }
        .user-message {
            background-color: #28A745;
            color: white;
            padding: 12px;
            border-radius: 10px;
            display: inline-block;
            max-width: 80%;
            font-size: 16px;
            font-family: Arial, sans-serif;
        }
        .ai-message {
            background-color: #444444;
            color: white;
            padding: 12px;
            border-radius: 10px;
            display: inline-block;
            max-width: 80%;
            font-size: 16px;
            font-family: Arial, sans-serif;
        }
    </style>
    """
    st.markdown(chat_css, unsafe_allow_html=True)

    # 2) Local Auto Voice Toggle
    if "ai_auto_voice" not in st.session_state:
        st.session_state["ai_auto_voice"] = False

    st.session_state["ai_auto_voice"] = st.checkbox(
        "Auto Voice Output (AI Chat)",
        value=st.session_state["ai_auto_voice"]
    )

    # 3) Initialize/Display Chat History
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    for msg in st.session_state["chat_history"]:
        container = "user-container" if msg["role"] == "user" else "ai-container"
        bubble = "user-message" if msg["role"] == "user" else "ai-message"
        st.markdown(
            f"""
            <div class="message-container {container}">
                <div class="{bubble}">{msg["content"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # 4) Clear Chat
    if st.button("🗑️ Clear Chat"):
        st.session_state["chat_history"] = []
        st.rerun()

    # 5) Chat Input
    user_query = st.chat_input("Type your message...")  # pinned=True if you're on Streamlit >= 1.22

    # 6) Handle new input
    if user_query:
        # a) Add user message
        st.session_state["chat_history"].append({"role": "user", "content": user_query})

        # b) Display user bubble
        st.markdown(
            f"""
            <div class="message-container user-container">
                <div class="user-message">{user_query}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # c) Stream AI response
        full_response = ""
        placeholder = st.empty()

        try:
            response = ollama.chat(
                model="llama3",  # or the model you want
                messages=[{"role": "user", "content": user_query}],
                stream=True
            )

            for chunk in response:
                full_response += chunk["message"]["content"]
                placeholder.markdown(
                    f"""
                    <div class="message-container ai-container">
                        <div class="ai-message">{full_response}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # d) Store final AI response
            st.session_state["chat_history"].append({"role": "assistant", "content": full_response})

            # e) Auto TTS if checkbox is on
            if st.session_state["ai_auto_voice"]:
                text_to_speech(full_response)

        except Exception as e:
            st.error("❌ Ollama API error.")
            st.code(str(e), language="bash")