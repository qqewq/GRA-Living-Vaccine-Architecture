"""Main simulation loop. See paper.tex for experimental setup."""
import yaml
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from agents import Agent, AgentState, Rule, RuleConditionClause
from signals import Environment


def load_agent_from_yaml(path: Path) -> Agent:
    data = yaml.safe_load(path.read_text())
    agent_cfg = data["agent"]
    state = AgentState({s["name"]: s["initial"] for s in agent_cfg.get("state", [])})
    rules = []
    for r in agent_cfg.get("rules", []):
        any_of = []
        for group in r["condition"]["any_of"]:
            group_clauses = [
                RuleConditionClause(c["type"], c["name"], c["op"], c["value"])
                for c in group["all_of"]
            ]
            any_of.append(group_clauses)
        rules.append(
            Rule(r["name"], any_of, r["action"]["type"], r["action"].get("params", {}))
        )
    stability_cfg = agent_cfg.get("stability", {})
    return Agent(agent_cfg["id"], state, rules, stability_cfg)


def main():
    agent_yaml = (
        Path(__file__).parent.parent / "dsl" / "examples" / "simple_immunotherapy.yaml"
    )
    agent = load_agent_from_yaml(agent_yaml)
    env = Environment()
    for t in range(30):
        env.update(t)
        signals = env.to_dict()
        result = agent.step(signals)
        print(
            f"t={t:2d} | inf={signals['infection_level']:.2f} | "
            f"act={result['state'].get('activation', 0):.2f} | null={result['nullified']}"
        )


if __name__ == "__main__":
    main()
