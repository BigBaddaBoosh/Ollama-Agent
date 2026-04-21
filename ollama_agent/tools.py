from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class ExecutionLog:
    task_id: int
    task_title: str
    output: str
    timestamp: str


class Toolbelt:
    @staticmethod
    def timestamp() -> str:
        return datetime.now(tz=timezone.utc).isoformat()

    @staticmethod
    def summarize(text: str, max_len: int = 400) -> str:
        if len(text) <= max_len:
            return text
        return text[: max_len - 3] + "..."
