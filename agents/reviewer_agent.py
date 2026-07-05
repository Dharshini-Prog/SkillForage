"""
ReviewerAgent - evaluates the generated skill against a quality rubric using Gemini.
"""

import os
import json
import logging
from typing import Dict, Any
from dotenv import load_dotenv
from google import genai
from shared.models import SkillBlueprint, ReviewResult
from utils.prompt_loader import load_prompt

# Setup logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

class ReviewerAgent:
    """
    ReviewerAgent uses Gemini to evaluate a generated Skill Package against its 
    original SkillBlueprint.
    """
    def __init__(self):
        load_dotenv()
        self.system_prompt = load_prompt("reviewer_prompt.md")
        
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            logger.warning("GOOGLE_API_KEY is not set. Gemini calls may fail.")
        self.client = genai.Client(api_key=api_key) if api_key else None

    def review(self, blueprint: SkillBlueprint, skill_package: Dict[str, str]) -> ReviewResult:
        """
        Orchestrates the LLM evaluation of a Skill Package against the SkillBlueprint.
        Returns a structured ReviewResult.
        """
        blueprint_json = blueprint.model_dump_json(indent=2)
        package_json = json.dumps(skill_package, indent=2)
        
        prompt = f"""
{self.system_prompt}

SkillBlueprint (Requirements):
{blueprint_json}

Generated Skill Package (Files to review):
{package_json}
"""
        if not self.client:
            raise RuntimeError("Gemini Client is not initialized due to missing API key.")

        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )
            text = response.text.strip()
            
            # Clean markdown JSON formatting if present
            if text.startswith("```json"):
                text = text[7:]
            elif text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()

            raw_data = json.loads(text)
        except Exception as e:
            logger.error(f"Failed to generate or parse JSON from Gemini in ReviewerAgent: {e}")
            raw_data = {
                "sqi_score": 0.0,
                "passed": False,
                "revision_required": True,
                "strengths": [],
                "weaknesses": ["ReviewerAgent failed to output valid JSON. This is an internal error, please retry formatting."],
                "feedback": f"Reviewer JSON parsing failed. Error: {e}",
                "suggested_improvements": ["Return valid JSON without syntax errors."]
            }

        normalized_data = self._normalize_review_data(raw_data)

        try:
            result = ReviewResult(**normalized_data)
            return result
        except Exception as e:
            logger.error(f"Failed to construct ReviewResult from normalized data: {e}")
            raise

    def _normalize_review_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Safely converts raw Gemini JSON output into the expected ReviewResult schema.
        Handles missing keys and coerces types.
        """
        normalized = {}
        
        # Numbers / Bools
        try:
            normalized["sqi_score"] = float(data.get("sqi_score", 0.0))
        except (ValueError, TypeError):
            normalized["sqi_score"] = 0.0
            
        normalized["passed"] = bool(data.get("passed", False))
        normalized["revision_required"] = bool(data.get("revision_required", True))
        
        # String fields
        feedback_val = data.get("feedback", "")
        normalized["feedback"] = str(feedback_val) if feedback_val else "No feedback provided."
        
        # List fields
        list_keys = ["strengths", "weaknesses", "suggested_improvements"]
        for key in list_keys:
            raw_list = data.get(key, [])
            if not isinstance(raw_list, list):
                raw_list = [raw_list] if raw_list else []
            normalized[key] = [str(item) for item in raw_list]
            
        return normalized