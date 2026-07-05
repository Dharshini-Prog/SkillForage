"""
PlannerAgent - creates a structured Skill Blueprint.

Documentation:
PlannerAgent designs the blueprint for a skill based on a user's request.
SkillBlueprint is the shared contract between all agents.
"""
import os
import json
import logging
from dotenv import load_dotenv
from google import genai
from typing import Union, List, Any, Dict
from shared.models import SkillBlueprint, ParsedRequest
from utils.prompt_loader import load_prompt

# Setup basic logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

class PlannerAgent:
    def __init__(self):
        load_dotenv()
        self.system_prompt = load_prompt("planner_prompt.md")
        
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            logger.warning("GOOGLE_API_KEY is not set. Gemini calls may fail.")
        self.client = genai.Client(api_key=api_key) if api_key else None

    def plan(self, parsed_request: ParsedRequest) -> Union[SkillBlueprint, List[str]]:
        if self._needs_clarification(parsed_request):
            return self._generate_clarification_questions(parsed_request)

        # Build prompt from parsed request details
        prompt = f"""
{self.system_prompt}

User Request Details:
Goal: {parsed_request.goal}
Domain: {parsed_request.domain}
Skill Type: {parsed_request.skill_type}
Target Users: {', '.join(parsed_request.target_users)}
Expected Outputs: {', '.join(parsed_request.expected_outputs)}
Constraints: {', '.join(parsed_request.constraints)}
Required Tools: {', '.join(parsed_request.required_tools)}
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
            logger.error(f"Failed to generate or parse JSON from Gemini: {e}")
            logger.error(f"Raw response was: {response.text if 'response' in locals() else 'None'}")
            raise

        # Normalize the raw data to gracefully match the schema
        normalized_data = self._normalize_blueprint_data(raw_data)

        # Validate and construct the SkillBlueprint
        try:
            blueprint = SkillBlueprint(**normalized_data)
            return blueprint
        except Exception as e:
            logger.error(f"Failed to construct SkillBlueprint from normalized data: {e}")
            raise

    def _needs_clarification(self, parsed_request: ParsedRequest) -> bool:
        return bool(parsed_request.missing_information)

    def _generate_clarification_questions(self, parsed_request: ParsedRequest) -> List[str]:
        return [
            f"Please provide more detail about: {info}"
            for info in parsed_request.missing_information
        ]

    def _normalize_blueprint_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Safely converts raw Gemini JSON output into the expected schema.
        Handles missing keys and coerces dictionaries into strings when lists of strings are expected.
        """
        normalized = {}
        
        # String fields
        string_keys = ["title", "description", "purpose", "example_prompt", "expected_response"]
        for key in string_keys:
            val = data.get(key, "")
            normalized[key] = str(val) if val else f"Generated {key}"
            
        # List of strings fields
        list_keys = [
            "target_users", "inputs", "outputs", "required_tools", 
            "workflow_steps", "constraints", "failure_cases", "success_criteria"
        ]
        
        for key in list_keys:
            raw_list = data.get(key, [])
            if not isinstance(raw_list, list):
                # Wrap single strings into a list
                raw_list = [raw_list] if raw_list else []
                
            clean_list = []
            for item in raw_list:
                if isinstance(item, dict):
                    # If Gemini incorrectly returned an object, extract values and join them
                    clean_list.append(" ".join(str(v) for v in item.values()))
                else:
                    clean_list.append(str(item))
            
            normalized[key] = clean_list

        # Dict fields
        raw_metadata = data.get("metadata", {})
        normalized["metadata"] = raw_metadata if isinstance(raw_metadata, dict) else {}

        return normalized