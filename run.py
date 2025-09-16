#!/usr/bin/env python3
"""
English Teacher Agent - Main Runner Script
"""

import subprocess
import sys
import os
from pathlib import Path

def check_requirements():
    """Check if required packages are installed."""
    try:
        import streamlit
        import openai
        import dotenv
        print("✅ All required packages are installed.")
        return True
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        return False

def check_env_file():
    """Check if .env file exists and has API key."""
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  .env file not found.")
        print("Please create a .env file with your OpenAI API key:")
        print("OPENAI_API_KEY=your_api_key_here")
        return False
    
    # Check if API key is set
    with open(env_file, 'r') as f:
        content = f.read()
        if "your_api_key_here" in content or "OPENAI_API_KEY=" not in content:
            print("⚠️  Please set your OpenAI API key in the .env file")
            return False
    
    print("✅ Environment configuration looks good.")
    return True

def main():
    """Main function to run the English Teacher Agent."""
    print("🚀 Starting English Teacher Agent...")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check environment
    if not check_env_file():
        print("\n📝 Setup Instructions:")
        print("1. Copy env_example.txt to .env")
        print("2. Add your OpenAI API key to the .env file")
        print("3. Run this script again")
        #sys.exit(1)
    
    print("\n🌐 Starting Streamlit app...")
    print("The app will open in your default browser.")
    print("Press Ctrl+C to stop the server.")
    print("=" * 50)
    
    try:
        # Run streamlit app
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n👋 English Teacher Agent stopped. Goodbye!")
    except Exception as e:
        print(f"❌ Error running the app: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
