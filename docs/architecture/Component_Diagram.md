# Component Diagram

```
          User
            │
            ▼
      Streamlit UI
            │
            ▼
       ADK Root Agent
            │
    ┌───────┴────────┐
    ▼                ▼
Planner Agent   Generator Agent
                     │
                     ▼
              Reviewer Agent
                     │
                     ▼
                 Exporter
                     │
                     ▼
                Generated Files
```

## Components

- User Interface
- Root Agent
- Planner Agent
- Generator Agent
- Reviewer Agent
- Exporter
- Generated Skill Package