# SkillForge

## Tagline
An AI agent that helps developers build better AI agent skills.

## Problem Statement
Writing high-quality SKILL.md files is difficult. Developers often miss workflow steps, tool selection, safety constraints, failure cases, and examples, leading to unreliable AI agents.

## Target Users
- AI Developers
- Agent Builders
- Hackathon Teams
- Students learning AI Agents

## Goal
Transform a rough natural-language idea into a production-ready SKILL.md through planning, generation, evaluation, and refinement.

## Input
A natural language description of a skill.

Example:
"Create a skill for an agent that summarizes research papers."

## Output
- SKILL.md
- Quality Report
- Evaluation Score
- Suggested Improvements

## Agents

### Root Agent
Coordinates the entire workflow.

### Planner Agent
Converts the user request into a structured blueprint.

### Skill Generator Agent
Generates the first version of SKILL.md.

### Reviewer Agent
Evaluates, scores, and refines the generated skill until it meets the quality threshold.

## MCP
- Filesystem MCP
- SQLite MCP
- GitHub MCP (optional)

## AI Model
Gemini

## Workflow

User
↓
Planner
↓
Skill Generator
↓
Reviewer
↺ Refine if needed
↓
Export

## Success Criteria
- Produces a valid SKILL.md
- Includes required sections
- Provides an evaluation score
- Improves weak drafts automatically