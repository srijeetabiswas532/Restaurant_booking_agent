# Restaurant_agent
### Creating a conversational agent that will allow the end-user to communicate and book a restaurant appointment.

May 15, 2025:
**Day 1:** I am building a restaurant agent (and eventually planning on hosting it!). Will be jotting down new things I learn here and will update later to a real README when I finish this project.

**CONCEPTUAL/LEARNING**
* What is an agent exactly - how does it differ from a simple LLM? or RAG-augmented LLM? 
* How does an agent use tools or does a web search? What part of this is the LLM and which parts is it a framework like Langchain
* How does the LLM know how to predict tool usage as next tokens?
* What is Langchain? 
* When you allow an agent access to a tool like "web search", Langchain/AutoGen is actually using a real-time API in the backend.
* What is Vertex AI?
* How the LLM processes tool descriptions as prompts
* Shared memory & session states in agentic frameworks
* AdkApp & wrapping your agents
* What is Cloudrun? What are its usecases & pros?
* How is Cloudrun different from Kubernetes?
* What is a POST/GET request?
* What is a CURL command? (Client URL)
* What is Agentspace?

**BUILDING**
* Tools used: gemini-pro (vertex AI; free), langchain (agent logic), flask + python (HTTP POST endpoint), cloud run (hosting), streamlit (front-end)
* create an .env file to store your API keys/config variables
* you ALWAYS need an API key when using models
* imports from typing are type hint helpers: useful for documentation, industry-standard code, not necessary for code to run
* gemini-pro is free (rn) and chatgpt gives you a free trial of gpt-3.5
* zero-shot-react-description

**Day 2:** Mostly troubleshooting pushing onto github & connecting with GCLOUD so I can use the gemini model.
* When linking to the remote github repo for the first time, it is better to initialize the repo from the command line or have a completely empty github repo remotely (otherwise there will be contradictions)
* GCLOUD requires a lot of authentication and billing
* You cannot push anything with a KEY to github (especially if it's public for security reasons)
* gemini-pro model can only work in certain locations
* better to have billing account and project account be on one account

* YOU LEFT OFF RUNNING YOUR AGENT.PY SCRIPT, YOU NEED TO ENABLE GENERATIVE AI IN YOUR GCLOUD ACCOUNT. THIS HAPPENS BECAUSE GOOGLE RESTRICTS GEMINI ACCESS PER PROJECT, EVEN IF VERTEXAI IS ENABLED. 