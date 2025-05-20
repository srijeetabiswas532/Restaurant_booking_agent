# Restaurant_agent
### Creating a conversational agent that will allow the end-user to communicate and book a restaurant appointment. Working for only 1-2 hours a day.

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

**Day 3:** Actually begin changing the skeleton code to create a functioning agent.
* pydantic: used it's BaseModel to help create a structured tool so it forces the LLM to output structured input (less parsing needed). This helps a ton with debugging, less hallucinated fields.
* Agent type ZERO SHOT AGENT requires your tools to only have 1 input. If you instead want your tools to have multi-structured input, use STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION
* multi-turn conversational behavior: agent prompts the user with questions when it is lacking information instead of returning a static message. Right now, my agent has no memory - so when the LLM does not have all the information, it just exits.
    * with a conversation loop / memory, it can ask and remember your response and continue.
    * AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION: this type of agent permits memory & tool usage. Langchain does not yet have a conversational agent that supports multi-input, structured tools.
* The reason why the LLM thinks and outputs in a structured JSON-like way, is because internally, LangChain uses a system prompt like this: 
    ''' You are a helpful assistant that can reason and use tools.
        When you decide to use a tool, respond in this format:
        ```json
        {
        "action": "tool_name",
        "action_input": "the input string for the tool"
        }
        '''
    * This is super helpful because (1) there is a clear separation between reasoning, tool-use, and final answers (2) easy for LC to parse through to detect tools to call, pass the right input, and know when to stop
    * Also very helpful in debugging as you can see the LLM's internal logic in a structured way
* FastAPI defines the routes, logic, and data models; Uvicorn actually serves these routes over HTTP; together they let you write code that accepts HTTP requests, processes data (booking info), and returns JSON responses.
* REST is an architectural style for designing APIs that use HTTP methods like GET, POST, PUT, and DELETE to interact with resources like users, reservations, products, etc.
    * Exposing a POST /book route in FastAPI means you are saying "Clients can use this to create a booking (resource)"
* An API endpoint is a specific URL + HTTP method combo (POST http://localhost:8000/book)
* Flow: (1) LLM decides to call book_reservation() (via LangChain) (2) Tool formats this input & sends a POST request (3) Uvicorn receives this request over http and transfers to fastAPI (4) FastAPI then (4a) Matches the request to @app.post('/book') route (4b) Uses pydantic's Reservation model to parse the JSON and (4c) Calls the book(reservation) function with the parsed object (5) The response generated by my function -> FastAPI -> uvicorn -> back to the client (my agent)
* When using FastAPI, you can go to the local port http://127.0.0.1:8000**/docs** and see what is going on under the hood - pretty interesting. 