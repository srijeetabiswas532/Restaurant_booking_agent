# app.py
import streamlit as st
from agent import agent, memory

# Set Streamlit page config
st.set_page_config(page_title="Restaurant Reservation Agent", layout="wide")

st.title("🍽️ Restaurant Reservation Agent")
st.markdown("Chat with an assistant to find, check, and book restaurants.")

# Initialize chat history in Streamlit session
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat input from user
user_input = st.chat_input("Say something...")

if user_input:
    st.session_state.chat_history.append(("user", user_input))
    
    with st.spinner("Thinking..."):
        try:
            agent_response = agent.run(user_input)
        except Exception as e:
            agent_response = f"❌ Error: {e}"
    
    st.session_state.chat_history.append(("agent", agent_response))

# Render chat history
for role, msg in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(msg)

# Optional: Reset conversation
if st.button("🔄 Reset Conversation"):
    st.session_state.chat_history = []
    memory.clear()
    st.rerun()
