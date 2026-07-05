"""
Exporter tool.

Documentation:
Exporter saves artifacts.
"""

import os
from typing import Dict

def export_skill(skill_name: str, files: Dict[str, str]) -> str:
    """
    Writes every generated artifact into exports/<skill_name>/ and returns the path.
    """
    base_dir = os.path.join(os.path.dirname(__file__), '..', 'exports', skill_name)
    os.makedirs(base_dir, exist_ok=True)
    
    for filename, content in files.items():
        with open(os.path.join(base_dir, filename), 'w', encoding='utf-8') as f:
            f.write(content)
            
    return os.path.abspath(base_dir)
