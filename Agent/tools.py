from langchain.agents import Tool
from FinancialGoals.RAGToSQL.FabricsRAG import ask_fabric
import json
from datetime import datetime
from .memory import save_user_memory
from .memory import get_portfolio_from_memory

#Calcular the investement plan
def calculate_investment_plan(user_input: str) -> str:
    try:
        # Try to parse current input
        try:
            current_data = json.loads(user_input)
            client_id = current_data.get("client_id", "default_user")
        except json.JSONDecodeError:
            current_data = {"goal_data": {"type": user_input}}
            client_id = "default_user"

        # Retrieve portfolio data from vector store
        portfolio_data = get_portfolio_from_memory(client_id)

        # Combine current data with stored portfolio data
        combined_data = {
            "portfolio_data": portfolio_data.get("portfolio_data", {}),
            "goal_data": current_data.get("goal_data", {})
        }

        stocks = combined_data["portfolio_data"].get("stocks", "No stock data")
        goal = combined_data["goal_data"].get("type", "No goal specified")

        print(f"DEBUG: Calculating investment plan with stored data - stocks: {stocks}, goal: {goal}")

        return json.dumps({
            "status": "success",
            "plan": {
                "stocks": stocks,
                "goal": goal,
                "recommended_investment": "$10,000/year"
            }
        })

    except Exception as e:
        print(f"Error in calculate_investment_plan: {e}")
        return json.dumps({
            "status": "error",
            "message": f"Error calculating plan: {str(e)}",
            "plan": None
        })

# Risk Analysis Tools
def ask_initial_question(user_input: str) -> str:
    return "What are you looking for in terms of financial analysis or investment advice?"

# Get Stock data for a client
def get_stock_positioning(user_input: str) -> str:
    try:
        print("Starting get_stock_positioning...", user_input)
        client_id = user_input

        if user_input == "None":
            print("user_input is null")
            return json.dumps({
                "status": "error",
                "message": "Please provide your client ID.",
                "portfolio_data": None
            })

        # Simulating portfolio data fetch
        client_data = ask_fabric(
            f"Fetch all details for the client id {client_id} including their portfolios, assets, risk metrics, and recommended asset allocations."
        )

        # Structure the response as JSON
        portfolio_data = {
            "status": "success",
            "portfolio_data": {
                "stocks": client_data,
                "last_updated": datetime.now().isoformat()
            }
        }

        # Save portfolio data to vector store
        save_user_memory(
            client_id,
            f"Fetching portfolio data for client {client_id}",
            "Portfolio data retrieved successfully",
            portfolio_data
        )

        return json.dumps(portfolio_data)

    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": f"Error: {str(e)}",
            "portfolio_data": None
        })

# Ask for a financial Goal
def ask_financial_goal(user_input: str) -> str:
    try:
        # Parse existing data if available
        existing_data = json.loads(user_input) if user_input else {}

        return json.dumps({
            "status": "success",
            "message": "What are your specific financial goals?",
            "previous_data": existing_data
        })
    except:
        return "What are your specific financial goals? Please include target amount and timeline."

# Calculate the risk plan
def calculate_risk(user_input: str) -> str:
    return "Based on your portfolio, we calculate a risk score of 7/10 with moderate diversification metrics."

# Suggest risk plan
def suggest_risk_plan(user_input: str) -> str:
    return "To mitigate risks, we suggest diversifying further into bonds and international equities."

# Suggest Investment Plan
def suggest_investment_plan(user_input: str) -> str:
    return "Here’s a suggested investment plan tailored to your goal. Let us know if it meets your expectations."

# Handle user feedback
def handle_feedback(user_input: str) -> str:
    if "alternative" in user_input.lower():
        return "Here’s an alternative plan: 40% stocks, 40% bonds, and 20% savings for a more conservative approach."
    return "Great! Let us know if you have any further questions or concerns."

# Setup all the tools
def get_tools():
    return [
        Tool(
            name="Ask Initial Question",
            func=ask_initial_question,
            description="Starts the conversation to understand user requirements or set context."
        ),
        Tool(
            name="Get Stock Positioning",
            func=get_stock_positioning,
            description=(
                "Retrieves the user's stock portfolio data, based on the user id. If not available, asks the user to share their portfolio details."
            )
        ),
        Tool(
            name="Ask Financial Goal",
            func=ask_financial_goal,
            description="Queries the user about their financial goals, such as savings or retirement plans."
        ),
        Tool(
            name="Calculate Risk",
            func=calculate_risk,
            description=(
                "Analyzes the user's stock portfolio to calculate associated risks."
            )
        ),
        Tool(
            name="Suggest Risk Plan",
            func=suggest_risk_plan,
            description=(
                "Provides a risk mitigation plan based on the calculated risks in the user's portfolio."
            )
        ),
        Tool(
            name="Calculate Investment Plan",
            func=calculate_investment_plan,
            description="Creates a tailored investment plan based on user input and extracted portfolio data from Get Stock Positioning tool"
        ),
        Tool(
            name="Suggest Investment Plan",
            func=suggest_investment_plan,
            description="Recommends an investment plan aligned with the user's financial goals."
        ),
        Tool(
            name="Handle Feedback",
            func=handle_feedback,
            description="Processes user feedback and provides alternative plans or suggestions."
        ),
    ]

