import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Centralized configuration for FinancialNexus_Agentic_AI"""
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-api-key-here")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    # Microsoft Fabric Lakehouse Configuration
    FABRIC_SQL_ENDPOINT = os.getenv("FABRIC_SQL_ENDPOINT", "your-fabric-lakehouse.fabric.microsoft.com")
    FABRIC_DATABASE = os.getenv("FABRIC_DATABASE", "your-database-name")
    FABRIC_RESOURCE_URL = os.getenv("FABRIC_RESOURCE_URL", "your-resource-url")
    FABRIC_TOKEN = os.getenv("FABRIC_TOKEN", "your-azure-token-here")
    
    # Azure SQL Database Configuration (for data insertion)
    AZURE_SQL_SERVER = os.getenv("AZURE_SQL_SERVER", "your-azure-sql-server.database.windows.net")
    AZURE_SQL_DATABASE = os.getenv("AZURE_SQL_DATABASE", "your-database-name")
    AZURE_SQL_USER = os.getenv("AZURE_SQL_USER", "your-username")
    AZURE_SQL_PASSWORD = os.getenv("AZURE_SQL_PASSWORD", "your-password")
    AZURE_SQL_PORT = int(os.getenv("AZURE_SQL_PORT", "1433"))
    
    # Application Configuration
    APP_PORT = int(os.getenv("APP_PORT", "7001"))
    APP_DEBUG = os.getenv("APP_DEBUG", "True").lower() == "true"
    
    # Memory Configuration
    MEMORY_BASE_PATH = os.getenv("MEMORY_BASE_PATH", "./user_memory")
    
    # Database Driver Configuration
    SQL_DRIVER = os.getenv("SQL_DRIVER", "ODBC Driver 18 for SQL Server")
    
    @classmethod
    def validate_config(cls):
        """Validate that all required configuration is set"""
        required_vars = [
            "OPENAI_API_KEY",
            "FABRIC_SQL_ENDPOINT", 
            "FABRIC_DATABASE",
            "FABRIC_TOKEN"
        ]
        
        missing_vars = []
        for var in required_vars:
            if getattr(cls, var) in ["your-openai-api-key-here", "your-fabric-lakehouse.fabric.microsoft.com", 
                                   "your-azure-token-here", "your-resource-url", "your-database-name"]:
                missing_vars.append(var)
        
        if missing_vars:
            print(f"⚠️  Warning: The following configuration variables need to be set:")
            for var in missing_vars:
                print(f"   - {var}")
            print("\nPlease update your .env file or environment variables.")
            return False
        
        return True

# Create a .env template file
def create_env_template():
    """Create a .env template file for users to fill in"""
    env_template = """# FinancialNexus_Agentic_AI Configuration
# Copy this file to .env and fill in your actual values

# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-4o-mini

# Microsoft Fabric Lakehouse Configuration
FABRIC_SQL_ENDPOINT=your-fabric-lakehouse.fabric.microsoft.com
FABRIC_DATABASE=your-database-name
FABRIC_RESOURCE_URL=your-resource-url
FABRIC_TOKEN=your-azure-token-here

# Azure SQL Database Configuration (for data insertion)
AZURE_SQL_SERVER=your-azure-sql-server.database.windows.net
AZURE_SQL_DATABASE=your-database-name
AZURE_SQL_USER=your-username
AZURE_SQL_PASSWORD=your-password
AZURE_SQL_PORT=1433

# Application Configuration
APP_PORT=7001
APP_DEBUG=True

# Memory Configuration
MEMORY_BASE_PATH=./user_memory

# Database Driver Configuration
SQL_DRIVER=ODBC Driver 18 for SQL Server
"""
    
    with open(".env.template", "w") as f:
        f.write(env_template)
    
    print("✅ Created .env.template file. Copy it to .env and fill in your values.")

if __name__ == "__main__":
    create_env_template()
    Config.validate_config() 