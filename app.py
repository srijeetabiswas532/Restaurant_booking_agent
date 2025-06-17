# app.py
import streamlit as st
from agent import agent, memory
import re

# Set Streamlit page config
st.set_page_config(page_title="Restaurant Reservation Agent", layout="wide")
st.title("🍽️ Restaurant Reservation Agent")
st.markdown("Chat with an assistant to find, check, and book restaurants.")

# -----------------------
# Email Input
# -----------------------
def is_valid_email(email: str) -> bool:
    # return re.match(r"[^@]+@[^@]+\\.[^@]+", email) is not None
    return True if email not in [None, ' ', ''] else False

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

st.session_state.user_email = st.text_input(
    "Your email (to receive confirmation)",
    value=st.session_state.user_email,
    placeholder="you@example.com"
)

if not is_valid_email(st.session_state.user_email):
    st.warning("⚠️ Please enter a valid email before chatting.")

# Initialize chat history in Streamlit session
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "restaurant_choices" not in st.session_state: # helps keep the memory
    st.session_state.restaurant_choices = []

# Handle search request directly
def handle_restaurant_selection(name: str):
    # Store name in LangChain memory directly
    memory.chat_memory.add_user_message(f"I choose {name}")
    memory.chat_memory.add_ai_message(f"Great! I'll use {name} as the restaurant for future steps.")
    
    st.session_state.chat_history.append(("user", f"I choose {name}"))
    st.session_state.chat_history.append(("agent", f"Great! I'll use **{name}** for future steps like checking availability or booking."))
    # Clear restaurant choices after selection
    st.session_state.restaurant_choices = []
    st.rerun()

# -----------------------
# Chat Input Handling
# -----------------------
user_input = st.chat_input("Ask me to search, check, or book a restaurant...")

if user_input and is_valid_email(st.session_state.user_email):
    st.session_state.chat_history.append(("user", user_input))

    with st.spinner("Thinking..."):
        try:
            response = agent.run({
                "input": user_input
                # "email": st.session_state.user_email
            })
            agent_response = response
        except Exception as e:
            agent_response = f"❌ Error: {e}"

    st.session_state.chat_history.append(("agent", agent_response))
    if "Reservation confirmed" in agent_response:
        st.success(f"📧 Confirmation email sent to {st.session_state.user_email}")


# Display conversation
for role, msg in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(msg)

# Show restaurant choices as buttons
if st.session_state.restaurant_choices:
    st.markdown("### 🍽️ Choose a restaurant:")
    for r in st.session_state.restaurant_choices:
        if st.button(r["name"]):
            handle_restaurant_selection(r["name"])

# Reset button
if st.button("🔄 Reset Conversation"):
    st.session_state.chat_history = []
    st.session_state.restaurant_choices = []
    memory.clear()
    st.rerun()
