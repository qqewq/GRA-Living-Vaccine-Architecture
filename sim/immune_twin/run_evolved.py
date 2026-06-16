"""
Evolved run for Immune GRA-Twin using evolutionary strategies.

Goal:
- Search for GRA-swarm configurations (n_scouts, n_nullifiers, n_memory, radii, thresholds)
  that minimize the integral of global foam Φ(t) over time.

This is a simple example using a hand-rolled ES-style search.
Later можно заменить на DEAP / Nevergrad / другой оптимизатор.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Tuple, List

from .environment import ImmuneTwin


# ---------------------------------------
# Parameter encoding for GRA-swarm
# ---------------------------------------

@dataclass
class SwarmConfig:
    n_scouts: int
    n_nullifiers: int
    n_memory: int

    scout_radius: float
    nullifier_radius: float
    nullifier_step: float

    scout_phi_threshold: float
    memory_phi_threshold: float


def clamp_int(x: float, lo: int, hi: int) -> int:
    return max(lo, min(hi, int(round(x))))


def clamp_float(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


# ---------------------------------------
# Fitness evaluation
# ---------------------------------------

def evaluate_config(
    cfg: SwarmConfig,
    n_steps: int = 200,
    n_tumor: int = 50,
    seed: int | None = None,
) -> float:
    """
    Run ImmuneTwin with given swarm config and return fitness.

    Fitness = integral Φ(t) over time (the lower, the better),
    plus small penalties for too large swarms (to favor elegant coordination).
    """

    model = ImmuneTwin(
        n_tumor=n_tumor,
        n_scouts=cfg.n_scouts,
        n_nullifiers=cfg.n_nullifiers,
        n_memory=cfg.n_memory,
        seed=seed,
    )

    # Inject parameters into agents
    for scout in model.scouts:
        scout.detection_radius = cfg.scout_radius
        # threshold, при котором Scout зовёт Nullifier
        scout.local_phi_threshold = cfg.scout_phi_threshold

    for nullifier in model.nullifiers:
        nullifier.null_radius = int(cfg.nullifier_radius)
        nullifier.step_size = cfg.nullifier_step

    for mem in model.memories:
        mem.reactivation_phi_threshold = cfg.memory_phi_threshold

    phi_sum = 0.0

    for _ in range(n_steps):
        model.step()
        phi_sum += model.global_phi

    # Penalty for large swarm size (we want elegant, not brute-force)
    swarm_size = cfg.n_scouts + cfg.n_nullifiers + cfg.n_memory
    penalty = 0.01 * swarm_size

    return phi_sum + penalty


# ---------------------------------------
# Simple evolutionary search
# ---------------------------------------

def random_config() -> SwarmConfig:
    return SwarmConfig(
        n_scouts=random.randint(3, 30),
        n_nullifiers=random.randint(5, 60),
        n_memory=random.randint(1, 15),
        scout_radius=random.uniform(5.0, 25.0),
        nullifier_radius=random.uniform(1.0, 8.0),
        nullifier_step=random.uniform(1.0, 4.0),
        scout_phi_threshold=random.uniform(0.5, 4.0),
        memory_phi_threshold=random.uniform(0.5, 4.0),
    )


def mutate(cfg: SwarmConfig, sigma: float = 0.3) -> SwarmConfig:
    """Gaussian-like mutation in log-space for some params, clamped to sane bounds."""

    def jitter_int(val, lo, hi):
        return clamp_int(val + random.gauss(0.0, sigma * (hi - lo)), lo, hi)

    def jitter_float(val, lo, hi):
        return clamp_float(val + random.gauss(0.0, sigma * (hi - lo)), lo, hi)

    return SwarmConfig(
        n_scouts=jitter_int(cfg.n_scouts, 3, 40),
        n_nullifiers=jitter_int(cfg.n_nullifiers, 5, 80),
        n_memory=jitter_int(cfg.n_memory, 1, 20),
        scout_radius=jitter_float(cfg.scout_radius, 3.0, 30.0),
        nullifier_radius=jitter_float(cfg.nullifier_radius, 1.0, 10.0),
        nullifier_step=jitter_float(cfg.nullifier_step, 0.5, 5.0),
        scout_phi_threshold=jitter_float(cfg.scout_phi_threshold, 0.1, 6.0),
        memory_phi_threshold=jitter_float(cfg.memory_phi_threshold, 0.1, 6.0),
    )


def evolutionary_search(
    n_generations: int = 20,
    population_size: int = 10,
    n_steps_eval: int = 200,
    n_tumor: int = 50,
    seed: int | None = 123,
) -> Tuple[SwarmConfig, float]:
    random.seed(seed)

    # Initial population
    population: List[SwarmConfig] = [random_config() for _ in range(population_size)]
    best_cfg: SwarmConfig | None = None
    best_fit: float = math.inf

    for gen in range(n_generations):
        scores: List[Tuple[float, SwarmConfig]] = []

        print(f"\n[GEN {gen}] evaluating population...")
        for idx, cfg in enumerate(population):
            fit = evaluate_config(cfg, n_steps=n_steps_eval, n_tumor=n_tumor, seed=seed)
            scores.append((fit, cfg))

            if fit < best_fit:
                best_fit = fit
                best_cfg = cfg

            print(
                f"  indiv {idx:02d} | "
                f"fit={fit:.2f} | "
                f"scouts={cfg.n_scouts} nullifiers={cfg.n_nullifiers} memory={cfg.n_memory}"
            )

        scores.sort(key=lambda x: x[0])

        print(
            f"[GEN {gen}] best in gen: "
            f"fit={scores[0][0]:.2f} (global best={best_fit:.2f})"
        )

        # Select top-k as parents
        k = max(2, population_size // 3)
        parents = [cfg for _, cfg in scores[:k]]

        # Create new population via mutation of parents
        new_population: List[SwarmConfig] = []
        while len(new_population) < population_size:
            parent = random.choice(parents)
            child = mutate(parent)
            new_population.append(child)

        population = new_population

    assert best_cfg is not None
    return best_cfg, best_fit


if __name__ == "__main__":
    best_cfg, best_fit = evolutionary_search(
        n_generations=10,
        population_size=8,
        n_steps_eval=150,
        n_tumor=40,
        seed=123,
    )

    print("\n=== BEST CONFIG FOUND ===")
    print(best_cfg)
    print(f"fitness (integral Φ + penalty) = {best_fit:.2f}")