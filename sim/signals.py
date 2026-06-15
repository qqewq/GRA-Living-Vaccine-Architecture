from dataclasses import dataclass
from typing import Dict


@dataclass
class Environment:
    infection_level: float = 0.0
    inflammation: float = 0.0

    def to_dict(self) -> Dict[str, float]:
        return {"infection_level": self.infection_level, "inflammation": self.inflammation}

    def update(self, t: int):
        # Periodic infection for demonstration
        self.infection_level = max(0.0, min(1.0, 0.5 + 0.5 * (t % 10) / 10.0))
        self.inflammation = max(0.0, min(1.0, 0.3 + 0.3 * ((t + 5) % 10) / 10.0))
