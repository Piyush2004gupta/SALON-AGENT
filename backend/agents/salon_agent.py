import sys, os
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_react_agent, Tool
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))
if BASE_DIR not in sys.path: sys.path.insert(0, BASE_DIR)


from llm.llm_service import llm
from retrieval.retriever import retrieve

from sheets_db import is_slot_available, get_available_slots, book_slot
def retrieve_context(query: str) -> str:
    chunks = retrieve(query)
    return "\n\n---\n\n".join([doc.page_content for doc in chunks])

class SalonAgent:
    def __init__(self):
        # Load system prompt
        with open(os.path.join(BASE_DIR, "prompts", "system_prompt.txt"), "r", encoding="utf-8") as f:
            system_prompt = f.read()

        # Tools
        self.tools = [
            Tool(name="KnowledgeBase", func=retrieve_context,
                 description="Answer questions about services, prices, hours, policies, locations, and addresses."),
            Tool(name="CheckAvailability",
                 func=lambda x: is_slot_available(*[i.strip() for i in x.split(',')]) if len(x.split(',')) == 3 else "Error: Input must be 'branch, date, time'",
                 description="Check slot availability. Input: branch, date (YYYY-MM-DD), time (HH:MM)."),
            Tool(name="GetAllAvailableSlots",
                 func=lambda x: get_available_slots(*[i.strip() for i in x.split(',')]) if len(x.split(',')) == 2 else "Error: Input must be 'branch, date'",
                 description="Get all available slots. Input: branch, date (YYYY-MM-DD)."),
            Tool(name="BookAppointment", func=self._safe_book,
                 description="Book appointment. Input: name, phone, branch, service, date, time."),
        ]

        # ReAct prompt
        template = f"""{system_prompt}

You have access to the following tools:
{{tools}}

Use the following format:
Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{{tool_names}}]
Action Input: the input to the action
Observation: the result of the action
... (repeat as needed)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!
Previous conversation history:
{{chat_history}}
Question: {{input}}
Thought:{{agent_scratchpad}}"""

        prompt = PromptTemplate.from_template(template)
        agent = create_react_agent(llm, self.tools, prompt)
        
        self.memory = ConversationBufferMemory(memory_key="chat_history")
        
        self.agent_executor = AgentExecutor(agent=agent, tools=self.tools,
                                            memory=self.memory,
                                            verbose=False, handle_parsing_errors=True, max_iterations=5)

    def _safe_book(self, x: str) -> str:
        # Split input string into 6 parts
        parts = [i.strip() for i in x.split(',')]
        if len(parts) != 6:
            return "Error: Need 6 values: name, phone, branch, service, date, time."

        name, phone, branch, service, date, time = parts

        # Call the database book_slot directly, which also checks availability
        return book_slot(name, phone, branch, service, date, time)

    def chat(self, query: str) -> str:
        # Send query to agent and return its response
        try:
            return self.agent_executor.invoke({"input": query})["output"].strip()
        except Exception as e:
            return f"Error: {str(e)}"

if __name__ == "__main__":
    agent = SalonAgent()
    print("LuxeGlow Assistant ready. Type 'exit' to quit.\n")
    while True:
        try:
            q = input("You: ")
            if q.lower() in ['exit', 'quit']: break
            print("Agent:", agent.chat(q))
        except (KeyboardInterrupt, EOFError):
            break
