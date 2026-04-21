from __future__ import annotations

import json
from pathlib import Path

from .models import Plan, Task


class PlanLoader:
    """Loads the project plan from JSON and validates required fields."""

    @staticmethod
    def load(path: str | Path) -> Plan:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        objective = data.get("objective", "")
        tasks = data.get("tasks", [])

        if not objective:
            raise ValueError("Plan file must include an objective")
        if not tasks:
            raise ValueError("Plan file must include at least one task")

        parsed = [
            Task(id=index + 1, title=item["title"], details=item.get("details", ""))
            for index, item in enumerate(tasks)
        ]
        return Plan(objective=objective, tasks=parsed)
