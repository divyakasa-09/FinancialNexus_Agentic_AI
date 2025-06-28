from langchain.agents import initialize_agent, AgentType
from langchain_community.chat_models import ChatOpenAI
from .tools import get_tools
from .memory import load_user_memory
from langchain.agents import AgentOutputParser
from langchain.schema import AgentAction, AgentFinish
import re
from typing import Union
import json
import sys
import os

# Add parent directory to path to import config
sys.path.append('../')
from config import Config

class JSONOutputParser(AgentOutputParser):
    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        try:
            # Regular parsing logic here
            action_match = re.search(r'Action: (.*?)[\n]', llm_output, re.DOTALL)
            action_input_match = re.search(r'Action Input: (.*?)[\n]', llm_output, re.DOTALL)

            if action_match and action_input_match:
                action = action_match.group(1).strip()
                action_input = action_input_match.group(1).strip()

                # Try to ensure action input is valid JSON when needed
                if action in ["Calculate Investment Plan", "Get Stock Positioning"]:
                    try:
                        # Verify it's valid JSON
                        json.loads(action_input)
                    except json.JSONDecodeError:
                        # If not valid JSON, wrap it in a basic structure
                        action_input = json.dumps({"user_input": action_input})

                return AgentAction(action, action_input, llm_output)

            # Return AgentFinish if no action is found
            return AgentFinish(
                return_values={"output": llm_output},
                log=llm_output,
            )
        except Exception as e:
            return AgentFinish(
                return_values={"output": f"Error parsing output: {str(e)}"},
                log=llm_output,
            )
def create_agent(user_id):
    llm = ChatOpenAI(model=Config.OPENAI_MODEL, temperature=0.1)
    tools = get_tools()
    PROMPT_TEMPLATE = """
    You are an intelligent financial advisor assistant. You must maintain context and pass data between tools using JSON formatting.

    CRITICAL WORKFLOW:
    1. ALWAYS start with Get Stock Positioning
    2. Parse the JSON response from Get Stock Positioning
    3. Combine the portfolio data with user goals when calling subsequent tools

    Data Handling Rules:
    - All tool inputs and outputs are JSON strings
    - You must parse tool responses before using them
    - When calling a new tool, include previous tool data in the request

    Example Correct Sequence:
    User: "I want to buy a house"
    Thought: Must get stock positioning first
    Action: Get Stock Positioning
    Action Input: new_user
    Observation: {{"status": "success", "portfolio_data": {{"stocks": "AAPL: 100, GOOGL: 50"}}}}
    Thought: Now I have the portfolio data, I'll calculate an investment plan
    Action: Calculate Investment Plan
    Action Input: {{"portfolio_data": {{"stocks": "AAPL: 100, GOOGL: 50"}}, "goal_data": {{"type": "house", "timeline": "5 years", "target_amount": "500000"}}}}

    Key Points:
    - ALL tool interactions must use JSON format
    - ALWAYS include previous tool data in subsequent calls
    - PARSE and VERIFY tool responses before proceeding

    Remember: Invalid or missing data handling:
    - If Get Stock Positioning returns error status, ask for more information
    - If data is incomplete, gather missing information before calculations
    - Always check status field in tool responses

    {tool_descriptions}
    """

    prompt = PROMPT_TEMPLATE.format(
        tool_descriptions="\n".join([f"{tool.name}: {tool.description}" for tool in tools]),
        chat_history="",
        input=""
    )

    # Create memory for the user
    memory, vectorstore = load_user_memory(user_id)
    # memory = HybridMemory(user_id)

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent="conversational-react-description",
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        memory=memory,
        verbose=True,
        prompt=prompt,
        handle_parsing_errors=True  # Add this to better handle errors
    )

    return agent