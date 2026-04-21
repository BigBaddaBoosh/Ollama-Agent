from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from .models import Plan, TaskStatus
from .ollama_client import OllamaClient
from .tools import ExecutionLog, Toolbelt


@dataclass
class SupportAgent:
    plan: Plan
    client: OllamaClient = field(default_factory=OllamaClient)
    history: List[ExecutionLog] = field(default_factory=list)

    def run(self) -> List[ExecutionLog]:
        while not self.plan.is_complete():
            task = self.plan.next_task()
            if task is None:
                break

            task.status = TaskStatus.IN_PROGRESS
            prompt = self._task_prompt(task.id, task.title, task.details)
            response = self.client.generate(prompt)

            if response.startswith("[OLLAMA_UNAVAILABLE]"):
                task.status = TaskStatus.BLOCKED
            else:
                task.status = TaskStatus.COMPLETE

            self.history.append(
                ExecutionLog(
                    task_id=task.id,
                    task_title=task.title,
                    output=Toolbelt.summarize(response),
                    timestamp=Toolbelt.timestamp(),
                )
            )

            if task.status == TaskStatus.BLOCKED:
                break

        return self.history

    def report(self) -> str:
        lines = [f"Objective: {self.plan.objective}"]
        for task in self.plan.tasks:
            lines.append(f"- [{task.status.value}] {task.id}. {task.title}")
        if self.history:
            lines.append("\nExecution log:")
            for entry in self.history:
                lines.append(f"  * ({entry.timestamp}) {entry.task_title}: {entry.output}")
        return "\n".join(lines)

    @staticmethod
    def _task_prompt(task_id: int, title: str, details: str) -> str:
        return (
            "You are an autonomous support engineering agent.\n"
            f"Task #{task_id}: {title}\n"
            f"Details: {details}\n"
            "Produce a concise action summary and recommended completion notes."
        )
