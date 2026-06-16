# Immune GRA-Twin

Immune GRA-Twin is an **agent-based in silico immune environment** inside the GRA-Living-Vaccine-Architecture.

It provides a minimal, testable model where:

- **Tumor / infection cells** emit local *foam* (chaotic pathological signal) into a 2D tissue/blood field.
- A **GRA-based swarm** of agents — `Scout`, `Nullifier`, `Memory` — coordinates to detect, suppress, and remember high-foam regions.
- A global foam metric **Φ(t)** is computed each step as the entropy of the foam field, showing how the system evolves under different swarm configurations.

The goal is to **verify GRA-Living-Vaccine-Architecture as a dynamical system**:  
a well-designed Scout + Nullifier + Memory swarm should drive Φ(t) down over time (pathology becomes unsustainable), while preserving local variability and adaptive behavior.

---

## Structure

```text
sim/
  immune_twin/
    __init__.py        # ImmuneTwin model export and module doc
    environment.py     # 2D continuous space, agents schedule, foam_field, global Φ
    agents.py          # TumorCell, Scout, Nullifier, Memory agent logic
    foam_metrics.py    # entropy() and compute_phi() for foam-field
    run_basic.py       # basic proof-of-concept: single run, Φ(t) plot
    run_evolved.py     # evolutionary search over swarm configs (optional, v0)
    README.md          # this file
```

---

## Basic usage

1. Install dependencies (from the root of the repo or from `sim/immune_twin`):

```bash
pip install mesa numpy matplotlib
```

2. Run the basic simulation:

```bash
cd sim/immune_twin
python run_basic.py
```

What happens:

- `ImmuneTwin` is initialized with:
  - a set of `TumorCell` agents emitting foam;
  - a GRA-swarm (`Scout`, `Nullifier`, `Memory`).
- The model runs for `N` steps.
- At each step, global foam **Φ(t)** is computed.
- A CSV with Φ(t) history and a PNG plot are written to `output/`.

You should see a curve where Φ(t) tends to decrease over time when the swarm is active, illustrating **GRA-driven nullification of pathological foam**.

---

## Evolved swarm configurations (optional)

`run_evolved.py` demonstrates how Immune GRA-Twin can be wrapped into a simple evolutionary search:

- A **SwarmConfig** encodes:
  - number of `Scout` / `Nullifier` / `Memory` agents,
  - radii and step sizes,
  - local Φ thresholds for reaction.
- The fitness function minimizes the **integral of Φ(t)** over the simulation horizon,  
  with a small penalty for very large swarms (favoring *elegant* coordination, not brute force).

Run:

```bash
cd sim/immune_twin
python run_evolved.py
```

This produces a log of generations and a “best found” configuration, giving a first glimpse of an **AI designer for living GRA-vaccines**.

---

## Relation to GRA-Living-Vaccine-Architecture

Immune GRA-Twin serves as the **in silico verification layer** for the architecture:

- It shows how GRA-defined agents (Scouts, Nullifiers, Memory cells) behave as a **self-organizing therapeutic swarm**.
- It provides concrete, reproducible metrics (Φ(t), swarm size, stability) that can be:
  - compared to baseline non-GRA controllers,
  - extended toward more realistic immune / oncology models,
  - integrated into **digital immune twins** and vaccine design workflows.

This makes GRA-Living-Vaccine-Architecture not only a conceptual framework,  
but a **testable computational system** that can evolve toward negentropic, disease-nullifying configurations.