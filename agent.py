import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_google_vertexai import ChatVertexAI
from google.cloud import aiplatform

from langchain.agents import Tool, initialize_agent
from langchain.agents.agent_types import AgentType
from langchain.memory import ConversationBufferMemory

# Import both tools
from tools import book_reservation_tool, check_availability_tool, search_restaurant_tool

# Load environment variables
load_dotenv()
project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
location = os.getenv("GOOGLE_CLOUD_LOCATION")

# Initialize Vertex AI
aiplatform.init(project=project_id, location=location)

# Use Gemini LLM
llm = ChatVertexAI(
    model_name="gemini-2.0-flash-001",
    temperature=0.7,
)

# Define tools (both multi-input)
tools = [
    search_restaurant_tool,
    check_availability_tool,
    book_reservation_tool
]

# Set up conversational memory
memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)

# Use agent type that supports multi-input structured tools
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    memory=memory,
    max_iterations=5,
    verbose=True
)

if __name__ == '__main__':
    print('Type "exit" to quit.')
    print('You are a helpful assistant that helps users search for restaurants, look for availability, and book restaurant reservations.')
    while True:
        user_input = input('You: ')
        if user_input.lower() in ['exit', 'quit']:
            memory.clear()
            break
        try:
            response = agent.run(user_input)
            print("Agent:", response)
        except Exception as e:
            print(f"❌ Error: {e}")
