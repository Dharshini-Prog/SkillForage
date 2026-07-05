"""
Prompt loading utility for SkillForge.
"""

import os

def load_prompt(prompt_filename: str) -> str:
    """
    Loads a Markdown file from the prompts directory.
    
    Documentation:
    These prompts will later become the system instructions supplied to Gemini 
    through ADK (Agent Development Kit).
    
    Returns:
        The content of the prompt file as a string. If the file cannot be loaded, 
        returns a clear placeholder string instead of raising an exception.
    """
    prompts_dir = os.path.join(os.path.dirname(__file__), '..', 'prompts')
    filepath = os.path.join(prompts_dir, prompt_filename)
    
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
    except Exception:
        pass
        
    return f"Placeholder for {prompt_filename} (file not found or could not be read)"
