"""
Agent definitions for GRA-Living-Vaccine simulator.
See paper.tex for architectural details.
"""

from dataclasses import dataclass
from typing import Dict, Any, List


@dataclass
class AgentState:
    values: Dict[str, float]


@dataclass
class RuleConditionClause:
    typ: str  # "signal" or "state"
    name: str
    op: str
    value: float

    def evaluate(self, signals: Dict[str, float], state: AgentState) -> bool:
        if self.typ == "signal":
            current = signals.get(self.name, 0.0)
        else:
            current = state.values.get(self.name, 0.0)

        if self.op == ">":
            return current > self.value
        if self.op == "<":
            return current < self.value
        if self.op == ">=":
            return current >= self.value
        if self.op == "<=":
            return current <= self.value
        if self.op == "==":
            return current == self.value
        if self.op == "!=":
            return current != self.value
        return False


@dataclass
class Rule:
    name: str
    any_of: List[List[RuleConditionClause]]
    action_type: str
    params: Dict[str, Any]

    def should_fire(self, signals: Dict[str, float], state: AgentState) -> bool:
        for group in self.any_of:
            if all(clause.evaluate(signals, state) for clause in group):
                return True
        return False


@dataclass
class Agent:
    id: str
    state: AgentState
    rules: List[Rule]
    stability_cfg: Dict[str, Any]
    nullified: bool = False
    soft_nullified: bool = False

    def step(self, signals: Dict[str, float]) -> Dict[str, Any]:
        if self.nullified:
            return {"nullified": True}
        if self.soft_nullified:
            return {"state": self.state.values, "soft_nullified": True}

        actions = []
        for rule in self.rules:
            if rule.should_fire(signals, self.state):
                self._apply_action(rule.action_type, rule.params, actions)

        self._check_stability()
        return {
            "actions": actions,
            "state": self.state.values,
            "nullified": self.nullified,
            "soft_nullified": self.soft_nullified,
        }

    def _apply_action(self, action_type: str, params: Dict[str, Any], actions: List[Dict[str, Any]]):
        if action_type == "therapeutic_effect":
            delta = params.get("delta_activation", 0.0)
            cost = params.get("cost_energy", 0.0)
            self.state.values["activation"] = min(
                1.0, max(0.0, self.state.values.get("activation", 0.0) + delta)
            )
            self.state.values["energy"] = max(
                0.0, self.state.values.get("energy", 0.0) - cost
            )
            actions.append({"type": "therapeutic_effect", "params": params})
        elif action_type == "change_state":
            delta = params.get("delta_activation", 0.0)
            self.state.values["activation"] = min(
                1.0, max(0.0, self.state.values.get("activation", 0.0) + delta)
            )
            actions.append({"type": "change_state", "params": params})
        elif action_type == "nullify":
            policy = params.get("policy", "hard")
            if policy == "love_oriented":
                actions.append({"type": "love_nullification", "params": params})
            self.nullified = True
            actions.append({"type": "nullify"})
        elif action_type == "love_transfer":
            frac = params.get("transfer_fraction", 0.8)
            self.state.values["energy"] *= (1 - frac)
            actions.append({"type": "love_transfer", "params": params})

    def _check_stability(self):
        max_act = self.stability_cfg.get("max_activation_level")
        if max_act is not None and self.state.values.get("activation", 0.0) > max_act:
            policy = self.stability_cfg.get("nullification_policy", {}).get("type", "hard")
            if policy == "hard":
                self.nullified = True
            elif policy == "soft":
                self.soft_nullified = True
                self.state.values["activation"] = 0.0
            elif policy == "love_oriented":
                self.nullified = True

        if self.state.values.get("energy", 1.0) <= 0.0:
            self.nullified = True
