"""
Evolutionary AI designer for GRA-Living-Vaccine.
See paper.tex Section 5.
"""
import random
from copy import deepcopy
from sim.agents import Agent, AgentState, Rule, RuleConditionClause
from sim.signals import Environment


def random_agent_template() -> Agent:
    state = AgentState({"energy": 0.5, "activation": 0.0})
    cond = RuleConditionClause(
        "signal", "infection_level", ">", random.uniform(0.3, 0.8)
    )
    rule = Rule(
        "auto_rule",
        [[cond]],
        "therapeutic_effect",
        {
            "delta_activation": random.uniform(0.05, 0.3),
            "cost_energy": random.uniform(0.05, 0.2),
        },
    )
    stability_cfg = {
        "max_activation_level": 1.0,
        "nullification_policy": {"type": "hard"},
    }
    return Agent("candidate", state, [rule], stability_cfg)


def evaluate_agent(agent: Agent, steps: int = 20) -> float:
    env = Environment()
    total = 0.0
    for t in range(steps):
        env.update(t)
        signals = env.to_dict()
        res = agent.step(signals)
        benefit = (1.0 - signals["infection_level"]) * (
            1.0 - res["state"].get("activation", 0.0)
        )
        total += benefit
        if res["nullified"]:
            total -= 1.0
            break
    return total


def mutate_agent(agent: Agent) -> Agent:
    child = deepcopy(agent)
    for rule in child.rules:
        if "delta_activation" in rule.params:
            rule.params["delta_activation"] *= random.uniform(0.8, 1.2)
        if "cost_energy" in rule.params:
            rule.params["cost_energy"] *= random.uniform(0.8, 1.2)
        for group in rule.any_of:
            for clause in group:
                if clause.typ == "signal" and clause.name == "infection_level":
                    clause.value = min(
                        1.0, max(0.0, clause.value + random.uniform(-0.1, 0.1))
                    )
    if random.random() < 0.2:
        love_rule = Rule(
            "love_on_low_energy",
            [[RuleConditionClause("state", "energy", "<", 0.2)]],
            "love_transfer",
            {"transfer_fraction": random.uniform(0.5, 0.9)},
        )
        child.rules.append(love_rule)
    return child


def evolve_population(pop_size: int = 10, generations: int = 5):
    population = [random_agent_template() for _ in range(pop_size)]
    for gen in range(generations):
        scores = [evaluate_agent(deepcopy(a)) for a in population]
        ranked = sorted(zip(scores, population), key=lambda x: x[0], reverse=True)
        print(
            f"Gen {gen}: best={ranked[0][0]:.3f}, avg={sum(scores)/len(scores):.3f}"
        )
        survivors = [deepcopy(a) for _, a in ranked[: pop_size // 2]]
        new_pop = []
        for s in survivors:
            new_pop.append(s)
            new_pop.append(mutate_agent(s))
        population = new_pop[:pop_size]
    best_score, best_agent = max(
        (evaluate_agent(deepcopy(a)), a) for a in population
    )
    print(f"Best final score: {best_score:.3f}")
    return best_agent


if __name__ == "__main__":
    best = evolve_population(generations=8, pop_size=12)
    print("Best agent rules:")
    for r in best.rules:
        print(f"  {r.name}: {r.action_type} {r.params}")
