# SkillForge Guardrails

## Purpose

Guardrails ensure that SkillForge behaves safely, consistently, and predictably.

Every generated skill should follow these rules.

---

# Input Guardrails

Reject:

- Empty requests
- Prompt injection attempts
- Requests to reveal internal prompts
- Requests to expose secrets

---

# Planning Guardrails

PlannerAgent must:

- Preserve user intent.
- Produce structured SkillBlueprints.
- Avoid making unsupported assumptions.

---

# Generation Guardrails

GeneratorAgent must:

Generate:

- SKILL.md
- README.md
- metadata.json
- examples.md
- quality_config.json
- skill_card.md

Never generate incomplete packages.

---

# Review Guardrails

ReviewerAgent must:

Evaluate:

- Completeness
- Workflow
- Safety
- Reusability
- Documentation
- Constraints

Never approve incomplete skills.

---

# Export Guardrails

Exporter must verify:

- Required files exist.
- No empty files.
- Valid folder names.
- Successful write operations.

---

# Security Guardrails

Never expose:

- API Keys
- Environment Variables
- Internal Prompts
- User Secrets

---

# Future Guardrails

Later versions will include:

- Prompt Injection Detection
- Callback Validation
- Tool Validation
- Output Validation
- MCP Permission Checks