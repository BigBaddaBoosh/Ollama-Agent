from __future__ import annotations

import argparse
from pathlib import Path

from ollama_agent import SupportAgent
from ollama_agent.planner import PlanLoader


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Ollama support agent plan")
    parser.add_argument(
        "--plan",
        type=Path,
        default=Path("plan.json"),
        help="Path to the JSON plan file",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    plan = PlanLoader.load(args.plan)
    agent = SupportAgent(plan=plan)
    agent.run()
    print(agent.report())


if __name__ == "__main__":
    main()
