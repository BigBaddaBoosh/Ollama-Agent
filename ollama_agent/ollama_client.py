from __future__ import annotations

import json
from dataclasses import dataclass
from urllib.error import URLError
from urllib.request import Request, urlopen


@dataclass
class OllamaClient:
    model: str = "llama3.1:8b"
    base_url: str = "http://localhost:11434"
    timeout: int = 60

    def generate(self, prompt: str) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }
        request = Request(
            f"{self.base_url}/api/generate",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        try:
            with urlopen(request, timeout=self.timeout) as response:
                body = json.loads(response.read().decode("utf-8"))
                return body.get("response", "").strip()
        except URLError as exc:
            return f"[OLLAMA_UNAVAILABLE] {exc}"
