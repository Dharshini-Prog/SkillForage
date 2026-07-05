"""
Smoke tests for the SkillForge multi-agent system.
"""

from agents.root_agent import RootAgent
from agents.planner_agent import PlannerAgent
from agents.generator_agent import GeneratorAgent
from agents.reviewer_agent import ReviewerAgent
from tools.request_parser import parse_request
from shared.models import ReviewResult

def test_request_parser_smoke():
    parsed = parse_request("Make a skill that summarizes text.")
    assert parsed.goal is not None

def test_planner_agent_smoke():
    parsed = parse_request("Make a skill")
    planner = PlannerAgent()
    blueprint = planner.plan(parsed)
    assert blueprint is not None

def test_generator_agent_smoke():
    parsed = parse_request("Make a skill")
    planner = PlannerAgent()
    blueprint = planner.plan(parsed)
    
    if not isinstance(blueprint, list):
        generator = GeneratorAgent()
        files = generator.generate(blueprint)
        assert "SKILL.md" in files
        assert "quality_config.json" in files

def test_root_agent_smoke():
    # Verify RootAgent initializes correctly
    root = RootAgent()
    assert hasattr(root, 'planner')
    assert hasattr(root, 'generator')
    assert hasattr(root, 'reviewer')

    # Execute the placeholder pipeline
    result = root.process_request("Create a skill.")
    
    # The current ReviewerAgent stub returns True for needs_revision (revision_required=True)
    # Thus, the export does NOT occur and a ReviewResult is returned
    assert isinstance(result, ReviewResult)
    assert result.revision_required is True

def test_root_agent_export_smoke():
    # Verify that export occurs only when the review passes
    root = RootAgent()
    
    original_review = root.reviewer.review
    
    # Mock the review to simulate a passing grade
    def mock_review(blueprint, skill_package):
        return ReviewResult(
            sqi_score=95.0,
            passed=True,
            revision_required=False,
            strengths=["Good structure"],
            weaknesses=[],
            feedback="Approved",
            suggested_improvements=[]
        )
    
    root.reviewer.review = mock_review
    
    result = root.process_request("Create a skill.")
    
    # Since revision_required is False, RootAgent should export and return (export_path, ReviewResult)
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert isinstance(result[0], str)  # Export path
    assert isinstance(result[1], ReviewResult)
    
    # Restore original function
    root.reviewer.review = original_review
