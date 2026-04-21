from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"
    BLOCKED = "blocked"


@dataclass
class Task:
    id: int
    title: str
    details: str
    status: TaskStatus = TaskStatus.PENDING


@dataclass
class Plan:
    objective: str
    tasks: List[Task] = field(default_factory=list)

    def next_task(self) -> Task | None:
        for task in self.tasks:
            if task.status in {TaskStatus.PENDING, TaskStatus.BLOCKED}:
                return task
        return None

    def is_complete(self) -> bool:
        return all(task.status == TaskStatus.COMPLETE for task in self.tasks)
