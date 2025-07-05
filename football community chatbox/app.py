#login page
import streamlit as st
import requests

FASTAPI_URL = "http://127.0.0.1:8000"

st.title("⚽ Football Community Chatbox")

import streamlit as st
import requests

FASTAPI_URL = "http://localhost:8000"  # or wherever your FastAPI is hosted

# User Login
st.subheader("Login to Chatbox")
username = st.text_input("Username")
password = st.text_input("Password", type="password")
login_placeholder = st.empty()

if st.button("Login"):
    response = requests.post(
        f"{FASTAPI_URL}/login",
        json={"username": username, "password": password}
    )
    
    if response.status_code == 200:
        st.session_state["logged_in_user"] = username
        login_placeholder.success("Login successful! You can now chat.")
    else:
        login_placeholder.error("Invalid username or password.")

# Check if user is logged in
if "logged_in_user" in st.session_state:
    st.subheader("Chat Messages")
    chat_placeholder = st.empty()
    warning_placeholder = st.empty()

    # Fetch and display messages without timestamps
    def load_messages():
        response = requests.get(f"{FASTAPI_URL}/display_community")
        if response.status_code == 200:
            messages = response.json()["messages"]
            formatted_chat = "\n".join([msg["message"] for msg in messages])
            chat_placeholder.text_area("Chat Window", formatted_chat, height=300, disabled=True)
        else:
            st.error("Failed to load messages.")

    load_messages()

    # Message input
    message = st.text_input("Type your message")

    # Send message
    if st.button("Send"):
        if message.strip():
            response = requests.post(f"{FASTAPI_URL}/community", json={"message": message})
            if response.status_code == 200:
                st.success("Message sent!")
                warning_placeholder.empty()
                load_messages()
            else:
                error_message = response.json().get("detail", "Error sending message.")
                if "Negative messages are not allowed" in error_message:
                    warning_placeholder.warning("⚠️ Negative messages are not allowed!")
                else:
                    st.error(error_message)
                