"""
RootAgent - receives user requests, invokes the Request Parser tool, and orchestrates the workflow.
"""

from typing import Union, Tuple
from tools.request_parser import parse_request
from tools.exporter import export_skill
from agents.planner_agent import PlannerAgent
from agents.generator_agent import GeneratorAgent
from agents.reviewer_agent import ReviewerAgent
from shared.models import ReviewResult
from utils.prompt_loader import load_prompt

class RootAgent:
    def __init__(self):
        self.system_prompt = load_prompt("root_prompt.md")
        self.planner = PlannerAgent()
        self.generator = GeneratorAgent()
        self.reviewer = ReviewerAgent()
        self.max_attempts = 3

    def process_request(self, request: str) -> Union[str, ReviewResult, Tuple[str, ReviewResult]]:
        """
        Orchestrates the pipeline with an autonomous review loop.
        """
        # 1. Parse Request
        parsed_request = parse_request(request)
        
        # 2. Plan (PlannerAgent designs)
        plan_result = self.planner.plan(parsed_request)
        
        # If the PlannerAgent returns clarification questions, stop the workflow
        if isinstance(plan_result, list):
            return "Clarification needed:\n" + "\n".join(plan_result)
            
        # 3 & 4. Generation and Review Loop
        attempts = 0
        skill_package = None
        review_result = None
        previous_feedback = None

        while attempts < self.max_attempts:
            print(f"--- Generation Attempt {attempts + 1} of {self.max_attempts} ---")
            
            # Generate (passing feedback if this is a retry)
            skill_package = self.generator.generate(plan_result, previous_feedback)
            
            # Review
            review_result = self.reviewer.review(plan_result, skill_package)
            
            if not review_result.revision_required:
                print("Review passed! Proceeding to export.")
                break
                
            print(f"Review failed. SQI Score: {review_result.sqi_score}")
            previous_feedback = review_result.feedback + "\nImprovements to make:\n" + "\n".join(review_result.suggested_improvements)
            attempts += 1
            
        if review_result.revision_required:
            print("Maximum attempts reached.")
            return review_result

        # 6. Export
        export_path = export_skill(plan_result.title, skill_package)
        print("Export completed successfully.")
        
        return export_path, review_result
