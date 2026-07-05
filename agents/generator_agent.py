"""
GeneratorAgent - converts the Skill Blueprint into a complete Skill Package using Gemini.
"""

import os
import json
import logging
from typing import Dict, Any
from dotenv import load_dotenv
from google import genai
from shared.models import SkillBlueprint
from utils.prompt_loader import load_prompt

# Setup logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

class GeneratorAgent:
    """
    GeneratorAgent transforms a SkillBlueprint into a complete Skill Package
    using a single Gemini LLM call, supporting feedback-driven refinement.
    """
    def __init__(self):
        load_dotenv()
        self.system_prompt = load_prompt("generator_prompt.md")
        
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            logger.warning("GOOGLE_API_KEY is not set. Gemini calls may fail.")
        self.client = genai.Client(api_key=api_key) if api_key else None

    def generate(self, blueprint: SkillBlueprint, previous_feedback: str = None) -> Dict[str, str]:
        """
        Accepts a SkillBlueprint and generates the complete skill package via Gemini.
        If previous_feedback is provided, it incorporates it to fix earlier issues.
        """
        blueprint_json = blueprint.model_dump_json(indent=2)
        
        prompt = f"""
{self.system_prompt}

SkillBlueprint Requirements:
{blueprint_json}
"""
        if previous_feedback:
            prompt += f"\n\nPREVIOUS REVIEW FEEDBACK TO ADDRESS:\n{previous_feedback}"
            
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
            logger.error(f"Failed to generate or parse JSON from Gemini in GeneratorAgent: {e}")
            raw_data = {
                "SKILL.md": f"CRITICAL ERROR: Failed to parse JSON from Generator. You must output valid JSON. Error: {e}",
            }

        # Normalize the raw data to ensure all 6 keys are present
        normalized = self._normalize_package_data(raw_data)
        return normalized

    def _normalize_package_data(self, data: Dict[str, Any]) -> Dict[str, str]:
        """
        Safely converts raw Gemini JSON output into the expected file dictionary schema.
        Handles missing keys by inserting fallbacks to prevent KeyErrors.
        """
        expected_keys = [
            "SKILL.md", "README.md", "examples.md", 
            "metadata.json", "quality_config.json", "skill_card.md"
        ]
        
        normalized = {}
        for key in expected_keys:
            val = data.get(key, "")
            # If Gemini accidentally gave an object/list instead of string, coerce it.
            if not isinstance(val, str):
                try:
                    val = json.dumps(val, indent=2)
                except Exception:
                    val = str(val)
            normalized[key] = val if val else f"# Placeholder for {key} due to missing generation"
            
        return normalized