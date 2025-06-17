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

# Chat input from user
user_input = st.chat_input("Ask me to search, check, or book a restaurant...")

if user_input:
    st.session_state.chat_history.append(("user", user_input)) # adding to memory
    
    with st.spinner("Thinking..."):
        try:
            response = agent.run(user_input)

            if isinstance(response, list) and (all ("name" in r for r in response) or all("options" in r for r in response) or all("Here are" in r for r in response)): # if agent response is top restaurant names
                st.write('buttons.')
                st.session_state.restaurant_choices = response
                agent_response = "Here are the top restaurants I found. Please choose one to book or check availability:"
            else: # else return agent response
                agent_response = response
        except Exception as e:
            agent_response = f"❌ Error: {e}"
    
    st.session_state.chat_history.append(("agent", agent_response)) # update chat history for the STREAMLIT UI display

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
