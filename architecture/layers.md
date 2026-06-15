# Architecture Layers

## Layer 0: Signal Environment
The external world modeled as a set of scalar signals: `infection_level`, `inflammation`, `toxicity`, etc. These evolve according to user-defined dynamics (e.g., periodic infection waves).

## Layer 1: DSL / Logic
Rules of the form `IF condition THEN action`. Conditions can check signals or internal state. Actions modify state or trigger nullification.

## Layer 2: Agent State
Each agent maintains:
- `activation`: therapeutic intensity (0.0 to 1.0)
- `energy`: metabolic resource (0.0 to 1.0)
- Additional user-defined variables

## Layer 3: Swarm
Multiple agents interact through:
- Signal broadcasting
- Energy transfer (love-oriented nullification)
- Collective stability computation

## Layer 4: AI Design Core
Evolutionary or Bayesian optimization of rule parameters and thresholds to maximize a fitness function balancing infection reduction and agent survival.
