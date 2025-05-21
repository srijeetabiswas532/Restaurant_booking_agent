import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import Tool, initialize_agent
from langchain.agents.agent_types import AgentType
from tools import book_reservation_tool

from langchain_google_vertexai import ChatVertexAI
from google.cloud import aiplatform

from langchain.memory import ConversationBufferMemory # adding conversational memory

# loading in API key from .env
load_dotenv()
# openai_api_k = os.getenv("OPEN_API_KEY")
project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
location = os.getenv("GOOGLE_CLOUD_LOCATION")

# initializing vertex ai SDK
aiplatform.init(project=project_id, location=location)

# # initializing LLM
# llm = ChatOpenAI(
#         temperature=0.7,
#         model_name='gpt-3.5-turbo',
#         openai_api_key=openai_ api_k
# )

# initializing LLM
llm = ChatVertexAI(
    model_name="gemini-2.0-flash-001",
    temperature=0.7,
)

# tools
tools = [
    book_reservation_tool
]

memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)

# initializing agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    # agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,  # it's structured chat (works with structured tools (multi-input))l; zero-shot (LLM decides tools based on descs, no examples); react (langchain agent framework); description (tool selection based off of text descs for each tool)
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True
)

if __name__ == '__main__':
    print('Type "exit" to quit.')
    while True:
        user_input = input('You: ')
        if user_input.lower() in ['exit', 'quit']:
            break
        response = agent.run(user_input)
        print("Agent: ", response)