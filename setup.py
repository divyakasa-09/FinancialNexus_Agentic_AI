#!/usr/bin/env python3
"""
Setup script for FinancialNexus_Agentic_AI
This script helps users configure the application with their credentials.
"""

import os
import sys
from pathlib import Path

def create_env_file():
    """Create .env file from template if it doesn't exist"""
    if os.path.exists('.env'):
        print("✅ .env file already exists.")
        return
    
    if os.path.exists('.env.template'):
        # Copy template to .env
        with open('.env.template', 'r') as template:
            content = template.read()
        
        with open('.env', 'w') as env_file:
            env_file.write(content)
        
        print("✅ Created .env file from template.")
        print("⚠️  Please edit .env file with your actual credentials.")
    else:
        print("❌ .env.template not found. Please run 'python config.py' first.")

def validate_installation():
    """Validate that all required packages are installed"""
    required_packages = [
        'flask',
        'langchain',
        'openai',
        'pyodbc',
        'faker',
        'pandas',
        'python-dotenv'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("Please run: pip install -r requirements.txt")
        return False
    else:
        print("✅ All required packages are installed.")
        return True

def check_configuration():
    """Check if configuration is properly set up"""
    try:
        from config import Config
        if Config.validate_config():
            print("✅ Configuration is properly set up.")
            return True
        else:
            print("❌ Configuration needs to be updated.")
            return False
    except Exception as e:
        print(f"❌ Error checking configuration: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 FinancialNexus_Agentic_AI Setup")
    print("=" * 40)
    
    # Step 1: Check Python version
    if sys.version_info < (3, 9):
        print("❌ Python 3.9+ is required.")
        return
    
    print("✅ Python version is compatible.")
    
    # Step 2: Validate installation
    if not validate_installation():
        return
    
    # Step 3: Create .env file
    create_env_file()
    
    # Step 4: Check configuration
    if not check_configuration():
        print("\n📝 Next steps:")
        print("1. Edit .env file with your credentials")
        print("2. Run 'python config.py' to validate configuration")
        print("3. Run 'python app.py' to start the application")
    else:
        print("\n🎉 Setup complete! You can now run 'python app.py'")

if __name__ == "__main__":
    main() 