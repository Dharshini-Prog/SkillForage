# Data Flow

## Step 1

User submits a skill generation request.

↓

## Step 2

Planner Agent converts the request into a structured Skill Blueprint.

↓

## Step 3

Generator Agent creates:

- SKILL.md
- README.md
- examples.md
- metadata.json
- quality_config.json
- skill_card.md

↓

## Step 4

Reviewer Agent evaluates quality.

↓

## Step 5

If review passes:

Export package.

Otherwise:

Regenerate until maximum attempts are reached.