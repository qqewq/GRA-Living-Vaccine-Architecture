from typing import List, Dict, Any
from sim.agents import Agent
from sim.signals import Environment


class Swarm:
    def __init__(self, agents: List[Agent]):
        self.agents = agents

    def step(self, env: Environment) -> List[Dict[str, Any]]:
        signals = env.to_dict()
        return [agent.step(signals) for agent in self.agents]

    # Love propagation can be implemented here
