import pyodbc
from faker import Faker
import random
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path to import config
sys.path.append('../')
from config import Config

# Database connection details - Using centralized configuration
server = Config.AZURE_SQL_SERVER
port = Config.AZURE_SQL_PORT
user = Config.AZURE_SQL_USER
password = Config.AZURE_SQL_PASSWORD
database = Config.AZURE_SQL_DATABASE

# Establish connection to the database
db = pyodbc.connect(
    f'DRIVER={{{Config.SQL_DRIVER}}};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'UID={user};'
    f'PWD={password};'
)

cursor = db.cursor()

# Initialize Faker
faker = Faker()

# Helper function to execute and commit queries
def execute_query(query, params=None):
    cursor.execute(query, params or [])
    db.commit()

# Insert data into Clients table
def populate_clients(num_clients=10):
    for _ in range(num_clients):
        name = faker.name()
        execute_query(
            "INSERT INTO Clients (Name) VALUES (?)",
            (name,)
        )

# Insert data into Assets table
def populate_assets(num_assets=20):
    asset_types = ['Equity', 'Bond', 'Real Estate', 'Commodity']
    for _ in range(num_assets):
        name = faker.company()
        asset_type = random.choice(asset_types)
        current_value = random.uniform(10000, 1000000)
        execute_query(
            "INSERT INTO Assets (Name, AssetType, CurrentValue) VALUES (?, ?, ?)",
            (name, asset_type, current_value)
        )

# Insert data into Portfolios table
def populate_portfolios(num_portfolios=10):
    cursor.execute("SELECT ClientID FROM Clients")
    client_ids = [row[0] for row in cursor.fetchall()]
    for _ in range(num_portfolios):
        name = f"Portfolio {faker.word().capitalize()}"
        client_id = random.choice(client_ids)
        risk_level = random.choice(['Low', 'Medium', 'High'])
        execute_query(
            "INSERT INTO Portfolios (Name, ClientID, RiskLevel) VALUES (?, ?, ?)",
            (name, client_id, risk_level)
        )

# Insert data into PortfolioAssets table
def populate_portfolio_assets():
    cursor.execute("SELECT PortfolioID FROM Portfolios")
    portfolio_ids = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT AssetID FROM Assets")
    asset_ids = [row[0] for row in cursor.fetchall()]
    for portfolio_id in portfolio_ids:
        num_assets = random.randint(1, 5)
        selected_assets = random.sample(asset_ids, num_assets)
        for asset_id in selected_assets:
            allocation = random.uniform(10, 50)  # Allocation in %
            execute_query(
                "INSERT INTO PortfolioAssets (PortfolioID, AssetID, Allocation) VALUES (?, ?, ?)",
                (portfolio_id, asset_id, allocation)
            )

# Insert data into FinancialGoals table
def populate_financial_goals():
    cursor.execute("SELECT ClientID FROM Clients")
    client_ids = [row[0] for row in cursor.fetchall()]
    financial_goals = [
        "Save $10,000 for an emergency fund within the next 12 months.",
        "Pay off all credit card debt by the end of this year.",
        "Contribute the maximum amount to retirement savings this year.",
        "Build a down payment of $30,000 for a first home purchase.",
        "Create a passive income stream that generates $500 per month.",
        "Save enough money to take a dream vacation to Europe.",
        "Start a college savings fund for my children.",
        "Invest in a diversified portfolio with a 7% annual return.",
        "Become completely debt-free within the next three years.",
        "Generate $20,000 in side hustle income annually.",
        "Save enough to start my own small business.",
        "Build an investment portfolio of $100,000 by retirement.",
        "Create a sustainable budget that allows for both savings and enjoyment.",
        "Save enough to cover six months of living expenses as an emergency fund.",
        "Invest in real estate and generate rental income.",
        "Reduce monthly expenses by 20% to increase savings rate.",
        "Save for early retirement by age 50.",
        "Create a long-term financial plan that supports generational wealth.",
        "Develop a strategy to pay off student loans within five years.",
        "Build a diversified investment portfolio that outperforms market averages."
    ]
    for client_id in client_ids:
        goal_description = random.choice(financial_goals)
        target_amount = random.uniform(50000, 500000)
        target_date = faker.date_between(start_date='today', end_date='+5y')
        execute_query(
            "INSERT INTO FinancialGoals (ClientID, GoalDescription, TargetAmount, TargetDate) VALUES (?, ?, ?, ?)",
            (client_id, goal_description, target_amount, target_date)
        )

# Insert data into RiskAssessmentMetrics table
def populate_risk_assessment_metrics():
    cursor.execute("SELECT AssetID FROM Assets")
    asset_ids = [row[0] for row in cursor.fetchall()]
    metrics = ['Volatility', 'Sharpe Ratio', 'Beta']
    for asset_id in asset_ids:
        for metric in metrics:
            value = random.uniform(0, 1)  # Example range for metrics
            timestamp = faker.date_time_between(start_date='-2y', end_date='now')
            execute_query(
                "INSERT INTO RiskAssessmentMetrics (AssetID, MetricName, Value, Timestamp) VALUES (?, ?, ?, ?)",
                (asset_id, metric, value, timestamp)
            )

# Insert data into RiskProfileMapping table
def populate_risk_profile_mapping():
    risk_levels = ['Low', 'Medium', 'High']
    asset_types = ['Equity', 'Bond', 'Real Estate', 'Commodity']
    for risk_level in risk_levels:
        for asset_type in asset_types:
            recommended_allocation = random.uniform(10, 50)  # Example allocation in %
            execute_query(
                "INSERT INTO RiskProfileMapping (RiskLevel, AssetType, RecommendedAllocation) VALUES (?, ?, ?)",
                (risk_level, asset_type, recommended_allocation)
            )

# Insert data into HistoricalProjections table
def populate_historical_projections():
    cursor.execute("SELECT PortfolioID FROM Portfolios")
    portfolio_ids = [row[0] for row in cursor.fetchall()]
    for portfolio_id in portfolio_ids:
        for _ in range(random.randint(5, 15)):
            date = faker.date_between(start_date='-1y', end_date='now')
            predicted_value = random.uniform(50000, 500000)
            actual_value = predicted_value * random.uniform(0.9, 1.1)  # Add variance
            execute_query(
                "INSERT INTO HistoricalProjections (PortfolioID, Date, PredictedValue, ActualValue) VALUES (?, ?, ?, ?)",
                (portfolio_id, date, predicted_value, actual_value)
            )

# Populate all tables
def main():
    populate_clients()
    populate_assets()
    populate_portfolios()
    populate_portfolio_assets()
    populate_financial_goals()
    populate_risk_assessment_metrics()
    populate_risk_profile_mapping()
    populate_historical_projections()

if __name__ == "__main__":
    main()
