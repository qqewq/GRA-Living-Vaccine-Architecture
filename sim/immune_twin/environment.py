"""
ImmuneTwin environment.

Agent-based in silico immune system for GRA-Living-Vaccine-Architecture.

- TumorCell / InfectionCell emit local foam (chaotic signal).
- Scout / Nullifier / Memory agents coordinate to reduce global foam Φ(t).
- Foam is represented as a 2D field over tissue/blood space.

This module defines the ImmuneTwin model and its main simulation loop.
"""

from mesa import Model
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation
import numpy as np

from .agents import TumorCell, Scout, Nullifier, Memory
from .foam_metrics import compute_phi


class ImmuneTwin(Model):
    """
    Basic immune twin model with:
    - continuous 2D space,
    - tumor / infection cells emitting foam,
    - GRA-based swarm agents acting on foam_field,
    - global_phi as system-level foam metric.
    """

    def __init__(
        self,
        width: int = 100,
        height: int = 100,
        n_tumor: int = 50,
        n_scouts: int = 10,
        n_nullifiers: int = 20,
        n_memory: int = 5,
        seed: int | None = None,
    ):
        super().__init__(seed=seed)

        self.width = width
        self.height = height

        # Continuous 2D tissue/blood space
        self.space = ContinuousSpace(width, height, torus=False)

        # Random activation schedule for agents
        self.schedule = RandomActivation(self)

        # Foam signal field (chaotic signal emitted by pathology)
        self.foam_field = np.zeros((width, height), dtype=float)
        self.global_phi: float = 0.0

        # Create tumor / infection cells
        for _ in range(n_tumor):
            cell = TumorCell(self)
            x = self.random.uniform(0, width)
            y = self.random.uniform(0, height)
            self.space.place_agent(cell, (x, y))
            self.schedule.add(cell)

        # Create GRA-based swarm agents
        self.scouts: list[Scout] = []
        for _ in range(n_scouts):
            scout = Scout(self)
            self.space.place_agent(
                scout,
                (self.random.uniform(0, width), self.random.uniform(0, height)),
            )
            self.schedule.add(scout)
            self.scouts.append(scout)

        self.nullifiers: list[Nullifier] = []
        for _ in range(n_nullifiers):
            nullifier = Nullifier(self)
            self.space.place_agent(
                nullifier,
                (self.random.uniform(0, width), self.random.uniform(0, height)),
            )
            self.schedule.add(nullifier)
            self.nullifiers.append(nullifier)

        self.memories: list[Memory] = []
        for _ in range(n_memory):
            mem = Memory(self)
            self.space.place_agent(
                mem,
                (self.random.uniform(0, width), self.random.uniform(0, height)),
            )
            self.schedule.add(mem)
            self.memories.append(mem)

    def step(self):
        """
        One simulation step:

        1) Tumor / infection cells emit foam into foam_field.
        2) Global foam Φ(t) is computed from foam_field.
        3) Swarm agents (Scout / Nullifier / Memory) update their state.
        """

        # Reset or decay foam field if нужно (например, лёгкое затухание)
        # Здесь пока просто оставляем накопление
        # self.foam_field *= 0.95

        # 1. Pathology emits foam
        for agent in self.schedule.agents:
            if isinstance(agent, TumorCell):
                agent.emit_foam()

        # 2. Compute global foam metric Φ(t)
        self.global_phi = compute_phi(self.foam_field)

        # 3. Let all agents act (Scouts / Nullifiers / Memories also modify foam_field)
        self.schedule.step()