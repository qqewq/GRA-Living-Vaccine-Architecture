"""
Immune GRA-Twin module for GRA-Living-Vaccine-Architecture.

This package implements an in silico immune environment where:
- TumorCell / InfectionCell emit local foam (chaotic signal),
- Scout / Nullifier / Memory agents form a GRA-based swarm,
- global foam Φ(t) is measured and driven down over time.

Use run_basic.py as an entry point for the simplest proof-of-concept simulation.
"""

from .environment import ImmuneTwin  # базовая модель среды