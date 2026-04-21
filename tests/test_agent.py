from ollama_agent.agent import SupportAgent
from ollama_agent.models import Plan, Task


class StubClient:
    def __init__(self, responses):
        self.responses = list(responses)

    def generate(self, prompt: str) -> str:
        return self.responses.pop(0)


def test_agent_completes_all_tasks_when_model_responds():
    plan = Plan(
        objective="test",
        tasks=[Task(id=1, title="one", details=""), Task(id=2, title="two", details="")],
    )
    agent = SupportAgent(plan=plan, client=StubClient(["done 1", "done 2"]))

    logs = agent.run()

    assert len(logs) == 2
    assert plan.is_complete()


def test_agent_blocks_when_ollama_unavailable():
    plan = Plan(objective="test", tasks=[Task(id=1, title="one", details="")])
    agent = SupportAgent(plan=plan, client=StubClient(["[OLLAMA_UNAVAILABLE] connection refused"]))

    logs = agent.run()

    assert len(logs) == 1
    assert plan.tasks[0].status.value == "blocked"
