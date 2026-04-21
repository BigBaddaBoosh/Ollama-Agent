# Ollama-Agent

Autonomous Support Agent that executes a structured plan with a local Ollama model.

## What this project includes

- A JSON-based project plan format (`plan.json`).
- A lightweight planning/execution loop with task tracking.
- A local Ollama client integration (`http://localhost:11434`).
- A CLI entrypoint for running the full workflow.
- Unit tests for the success and unavailable-model flows.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py --plan plan.json
```

## Example output

The agent prints:

- the objective,
- each task with status (`pending`, `in_progress`, `complete`, `blocked`),
- and a short execution log.

If Ollama is unavailable, the current task is marked `blocked` and execution stops gracefully.

## Project layout

```text
.
├── main.py
├── plan.json
├── ollama_agent/
│   ├── agent.py
│   ├── models.py
│   ├── ollama_client.py
│   ├── planner.py
│   └── tools.py
└── tests/
    └── test_agent.py
```
