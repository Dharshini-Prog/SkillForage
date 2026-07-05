# SkillForge Design Principles

## Purpose

SkillForge is a multi-agent system designed to help developers create high-quality, reusable AI Agent Skills.

Rather than generating skills in a single step, SkillForge follows a structured software engineering workflow consisting of planning, generation, review, refinement, and export.

Every architectural decision in SkillForge follows the principles below.

---

# Principle 1 – One Agent, One Responsibility

Each agent performs only one well-defined responsibility.

- RootAgent orchestrates.
- PlannerAgent designs.
- GeneratorAgent builds.
- ReviewerAgent evaluates and improves.

No agent should perform another agent's responsibility.

---

# Principle 2 – Preserve User Intent

The user's original request should never be changed.

Agents may improve quality but must never alter the requested objective.

---

# Principle 3 – Quality Before Speed

SkillForge prioritizes reliable, structured outputs over fast generation.

No skill should be exported without passing quality review.

---

# Principle 4 – Review Before Export

Every generated Skill Package must be reviewed.

Outputs that fail quality requirements must be refined before export.

---

# Principle 5 – Reusable Skills

Every generated skill should be reusable across different projects.

Avoid project-specific assumptions whenever possible.

---

# Principle 6 – Structured Communication

Agents communicate only through shared data models.

Current shared models include:

- ParsedRequest
- SkillBlueprint
- Skill Package

---

# Principle 7 – Safety First

Never expose secrets.

Never hallucinate APIs.

Never generate unsafe instructions.

Always include safety considerations when appropriate.

---

# Principle 8 – Modular Architecture

Every component should remain modular and replaceable.

Future improvements should not require rewriting existing components.

---

# Principle 9 – Explainable Decisions

Every major architectural decision should be documented through ADRs.

The system should remain understandable by future contributors.

---

# Principle 10 – Continuous Improvement

The ReviewerAgent continuously improves generated skills until the required quality threshold is reached.

SkillForge values iterative refinement over one-shot generation.