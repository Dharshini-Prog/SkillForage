"""
SkillForge - AI Agent Skills multi-agent system.
ADK Entry Point.
"""

import os
from dotenv import load_dotenv
from agents.adk_root_agent import ADKRootAgent
import logging

logging.basicConfig(level=logging.WARNING, force=True)

logging.getLogger("google_genai").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)

def main():
    # 1. Load configuration (including Gemini 2.5 Flash from .env)
    load_dotenv()

    
    # 2. Initialize the ADK Agent (which internally wraps RootAgent)
    adk_agent = ADKRootAgent()
    
    # 3. Simulate a startup request to prove it works
    print("Sending startup request...")
    response = adk_agent.run("Create a skill for an AI agent that summarizes research papers.")
    print(f"ADK Agent Response: {response}")

    
if __name__ == "__main__":
    main()
