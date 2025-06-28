def detect_intent(user_input: str, memory) -> str:
    """
    Determines whether the user is asking for risk analysis or investment planning based on the current input and user history.

    Args:
        user_input (str): The current input from the user.
        memory (ConversationBufferMemory): The memory object storing conversation history.

    Returns:
        str: The detected intent ("risk_analysis", "investment_planning", or "unknown").
    """

    # Fetch conversation history from memory
    user_history = memory.load_memory_variables({}).get("chat_history", "")

    # Define keyword sets for intents
    risk_keywords = {"risk", "diversify", "portfolio", "score", "hedge", "exposure", "volatility"}
    investment_keywords = {"investment", "portfolio", "plan", "goal", "return", "growth", "strategy", "savings"}

    # Combine history and user input for context
    combined_context = f"{user_history} {user_input}".lower()

    # Count keyword matches for each intent
    risk_score = sum(keyword in combined_context for keyword in risk_keywords)
    investment_score = sum(keyword in combined_context for keyword in investment_keywords)

    # Determine intent based on highest score
    if risk_score > investment_score:
        return "risk_analysis"
    elif investment_score > risk_score:
        return "investment_planning"
    else:
        return "unknown"