"""
Agents for Immune GRA-Twin.

- TumorCell / InfectionCell emit local foam (chaotic signal).
- Scout scans local foam and assigns targets to Nullifier agents.
- Nullifier moves to target and applies local GRA-nullification to foam_field.
- Memory records successfully nullified zones and triggers faster response on relapse.
"""

from __future__ import annotations

import numpy as np
from mesa import Agent

from .foam_metrics import entropy


class TumorCell(Agent):
    """
    Pathological cell (tumor / infected) that emits chaotic foam into foam_field.
    """

    def __init__(self, model):
        super().__init__(model)
        self.foam_strength: float = 10.0  # intensity of emitted chaos

    def emit_foam(self):
        """
        Add noisy signal around current position into model.foam_field.
        """
        x, y = int(self.pos[0]), int(self.pos[1])
        h = 3  # radius of influence

        for dx in range(-h, h + 1):
            for dy in range(-h, h + 1):
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.model.width and 0 <= ny < self.model.height:
                    self.model.foam_field[nx, ny] += np.random.normal(
                        0.0, self.foam_strength / 5.0
                    )

    def step(self):
        # Emission is called from model.step(); here можно ничего не делать
        pass


class Scout(Agent):
    """
    Scout agent:
    - scans local foam around itself,
    - computes local Φ,
    - if Φ is high, assigns a target for a free Nullifier.
    """

    def __init__(self, model):
        super().__init__(model)
        self.detection_radius: int = 10
        self.local_phi: float = 0.0

    def step(self):
        x, y = int(self.pos[0]), int(self.pos[1])
        r = self.detection_radius

        x_min = max(0, x - r)
        x_max = min(self.model.width, x + r)
        y_min = max(0, y - r)
        y_max = min(self.model.height, y + r)

        local_field = self.model.foam_field[x_min:x_max, y_min:y_max]

        if local_field.size > 0:
            self.local_phi = entropy(local_field.flatten())
        else:
            self.local_phi = 0.0

        # If local foam is high enough, request a Nullifier
        if self.local_phi > 2.0:  # TODO: tune threshold
            tx, ty = x, y
            for nullifier in self.model.nullifiers:
                if nullifier.target is None:
                    nullifier.target = (tx, ty)
                    nullifier.mode = "suppress"
                    break


class Nullifier(Agent):
    """
    Nullifier agent:
    - moves towards assigned target,
    - locally suppresses foam_field using a GRA-like operator,
    - when foam is low enough, clears target and notifies Memory agents.
    """

    def __init__(self, model):
        super().__init__(model)
        self.target: tuple[int, int] | None = None
        self.mode: str = "idle"
        self.step_size: float = 2.0
        self.null_radius: int = 3

    def step(self):
        if self.mode != "suppress" or self.target is None:
            return

        tx, ty = self.target
        dx = tx - self.pos[0]
        dy = ty - self.pos[1]
        dist = np.sqrt(dx * dx + dy * dy)

        # Move towards target
        if dist > 1e-6:
            nx = self.pos[0] + (dx / dist) * self.step_size
            ny = self.pos[1] + (dy / dist) * self.step_size
            self.model.space.move_agent(self, (nx, ny))

        # Apply local nullification (foam suppression) around current position
        x, y = int(self.pos[0]), int(self.pos[1])
        r = self.null_radius

        x_min = max(0, x - r)
        x_max = min(self.model.width, x + r + 1)
        y_min = max(0, y - r)
        y_max = min(self.model.height, y + r + 1)

        # Simple multiplicative suppression; позже можно заменить на более умный оператор
        self.model.foam_field[x_min:x_max, y_min:y_max] *= 0.2

        # Check if foam near target is sufficiently low
        tx_i = min(max(0, tx), self.model.width - 1)
        ty_i = min(max(0, ty), self.model.height - 1)
        if self.model.foam_field[tx_i, ty_i] < 0.5:
            # Notify memories about successful nullification
            for mem in self.model.memories:
                mem.record((tx, ty))

            # Reset state
            self.target = None
            self.mode = "idle"


class Memory(Agent):
    """
    Memory agent:
    - maintains a memory_map of zones that were previously nullified,
    - if foam reappears in a memorized zone, it quickly requests a Nullifier.
    """

    def __init__(self, model):
        super().__init__(model)
        self.memory_map = np.zeros((model.width, model.height), dtype=float)

    def record(self, pos: tuple[float, float]):
        """
        Record a successfully nullified region around pos.
        """
        x, y = int(pos[0]), int(pos[1])
        r = 5

        x_min = max(0, x - r)
        x_max = min(self.model.width, x + r + 1)
        y_min = max(0, y - r)
        y_max = min(self.model.height, y + r + 1)

        self.memory_map[x_min:x_max, y_min:y_max] = 1.0

    def step(self):
        """
        If foam reappears in memorized zones, request a Nullifier.
        """
        x, y = int(self.pos[0]), int(self.pos[1])

        # Clamp to bounds
        x = min(max(0, x), self.model.width - 1)
        y = min(max(0, y), self.model.height - 1)

        if self.memory_map[x, y] > 0 and self.model.foam_field[x, y] > 2.0:
            for nullifier in self.model.nullifiers:
                if nullifier.target is None:
                    nullifier.target = (x, y)
                    nullifier.mode = "suppress"
                    break