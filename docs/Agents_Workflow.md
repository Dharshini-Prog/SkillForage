# SkillForge Agent Workflow

## Overview

SkillForge follows a structured multi-agent workflow.

Instead of generating a skill in one prompt, the request passes through multiple specialized agents.

---

## Step 1 – User Request

The user submits a natural-language request describing the desired AI Agent Skill.

Example:

Create a research paper summarization skill.

---

## Step 2 – RootAgent

The RootAgent receives the request.

Responsibilities:

- Coordinate the workflow.
- Delegate tasks.
- Never generate content itself.

---

## Step 3 – Request Parser

The Request Parser converts the natural-language request into a structured ParsedRequest.

Output:

- Goal
- Domain
- Target Users
- Constraints
- Expected Outputs
- Required Tools

---

## Step 4 – PlannerAgent

PlannerAgent converts the ParsedRequest into a complete SkillBlueprint.

The blueprint defines:

- Purpose
- Workflow
- Inputs
- Outputs
- Constraints
- Failure Cases
- Success Criteria

---

## Step 5 – GeneratorAgent

GeneratorAgent converts the SkillBlueprint into a Skill Package.

Generated artifacts include:

- SKILL.md
- README.md
- examples.md
- metadata.json
- quality_config.json
- skill_card.md

---

## Step 6 – ReviewerAgent

ReviewerAgent evaluates the generated Skill Package.

Checks include:

- Completeness
- Clarity
- Tool usage
- Workflow
- Constraints
- Documentation
- Reusability

Reviewer calculates the Skill Quality Index (SQI).

If quality is below the threshold:

Generator receives improvement feedback.

The cycle repeats.

---

## Step 7 – Exporter

Once approved,

the Exporter saves the Skill Package into

exports/

and returns the final location.

---

## Final Output

The user receives:

- Reviewed Skill Package
- SQI
- Deployment Status
- Export Location