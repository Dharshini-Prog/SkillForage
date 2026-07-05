# Class Diagram

## Core Classes

```
ADKRootAgent
│
├── PlannerAgent
├── GeneratorAgent
├── ReviewerAgent
└── Exporter
```

### ADKRootAgent

Coordinates the complete workflow.

### PlannerAgent

Creates a structured Skill Blueprint from the user's request.

### GeneratorAgent

Generates all required skill artifacts.

### ReviewerAgent

Evaluates quality and provides feedback.

### Exporter

Writes generated files to the exports directory.

---

## Relationships

```
RootAgent
    │
    ├── PlannerAgent
    ├── GeneratorAgent
    ├── ReviewerAgent
    └── Exporter
```