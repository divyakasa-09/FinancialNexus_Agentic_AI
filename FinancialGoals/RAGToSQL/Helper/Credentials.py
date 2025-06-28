import sys
import os
sys.path.append('../../../')
from config import Config

class Credentials:
    """Credentials class that uses centralized configuration"""
    
    # SQL End point from Microsoft Fabric Lakehouse
    sql_endpoint = Config.FABRIC_SQL_ENDPOINT
    # Name of the database
    database = Config.FABRIC_DATABASE
    # Resource URL for Azure authentication
    resource_url = Config.FABRIC_RESOURCE_URL
    # Azure token for authentication
    token = Config.FABRIC_TOKEN
    # Open AI Key
    open_ai_key = Config.OPENAI_API_KEY
    # Model
    model = Config.OPENAI_MODEL

