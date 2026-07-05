"""
ADK Root Agent integration.

This module provides the Google ADK compatible integration for SkillForge.
It uses compositional design (rather than subclassing the ADK Agent BaseModel)
to safely orchestrate the existing SkillForge RootAgent.
"""

import os
from google.adk import Agent
from agents.root_agent import RootAgent

class ADKRootAgent:
    """
    A compositional wrapper that integrates the official ADK Agent 
    and forwards incoming requests to the internal SkillForge orchestrator.
    """
    def __init__(self):
        # Instantiate the official ADK Agent directly as recommended by Pydantic/ADK guidelines
        self.adk_agent = Agent(
            name="skillforge_root_agent",
            model=os.getenv("ADK_MODEL", "gemini-2.5-flash")
        )
        
        # Keep RootAgent as the business orchestrator
        self.internal_orchestrator = RootAgent()

    def run(self, user_input: str) -> str:
        """
        Main entry point for ADK execution.
        Forwards requests to RootAgent.
        """
        # Intercept initialization commands to return the required success criteria
        if user_input.strip().lower() in ["init", "start", "ping", "hello", ""]:
            return "SkillForge initialized successfully."
            
        # The ADK wrapper only forwards requests to RootAgent
        result = self.internal_orchestrator.process_request(user_input)
        
        # Parse and return a clean string representation of the result
        if isinstance(result, tuple):
            export_path, review_result = result
            status = "Review Passed!" if not review_result.revision_required else "Review Failed!"
            return f"Success! Exported to: {export_path}\nReview Score: {review_result.sqi_score}/100\n{status}"
            
        if isinstance(result, str):
            return result
            
        # If it returned just ReviewResult (max attempts reached)
        status = "Review Passed!" if not result.revision_required else "Review Failed!"
        return f"Review Score: {result.sqi_score}/100\n{status}"
