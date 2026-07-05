"""
Request Parser tool.

Role in the Multi-Agent Workflow:
---------------------------------
The Request Parser acts as the first line of structure in the SkillForge pipeline.
It takes a raw, unstructured natural-language request from the user (via the RootAgent)
and transforms it into a normalized `ParsedRequest` data model. 

This structured intermediate format ensures that the PlannerAgent receives clean, 
organized data (goal, domain, constraints, etc.) rather than having to interpret 
raw user text, decoupling intent extraction from skill planning.
"""

from shared.models import ParsedRequest

def parse_request(request: str) -> ParsedRequest:
    """
    Extracts the user's intent from a natural language request.
    
    Args:
        request: The raw user prompt or request.
        
    Returns:
        ParsedRequest: The structured representation of the user's intent.
        
    Note:
        LLM calls are not implemented yet. This currently returns a stubbed ParsedRequest.
    """
    # TODO: Implement LLM call to populate ParsedRequest based on `request`
    return ParsedRequest(
        goal="Extract intent from raw request",
        domain="General",
        skill_type="General",
        target_users=[],
        expected_outputs=[],
        constraints=[],
        required_tools=[],
        quality_requirements=[],
        missing_information=[]
    )
