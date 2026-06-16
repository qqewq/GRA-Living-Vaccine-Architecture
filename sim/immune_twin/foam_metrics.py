"""
Foam metrics for Immune GRA-Twin.

Defines:
- entropy()  : Shannon entropy for 1D array of foam values.
- compute_phi(): global foam Φ(t) as entropy of the foam_field.
"""

from __future__ import annotations

import numpy as np


def entropy(values: np.ndarray) -> float:
    """
    Shannon entropy (base 2) for a 1D array of values.

    We approximate the distribution with a histogram and compute:
        H = - sum p_i * log2(p_i)
    """
    if values.size == 0:
        return 0.0

    # Normalize values to avoid extreme outliers dominating bins
    v = values.astype(float)
    # Можно слегка обрезать по квантилям, если нужно
    # q_low, q_high = np.percentile(v, [1, 99])
    # v = np.clip(v, q_low, q_high)

    hist, _ = np.histogram(v, bins=32, density=True)
    hist = hist[hist > 0]

    if hist.size == 0:
        return 0.0

    return float(-np.sum(hist * np.log2(hist)))


def compute_phi(foam_field: np.ndarray) -> float:
    """
    Global foam metric Φ(t) as entropy of the entire foam_field.

    foam_field: 2D array [width, height] of foam values.
    """
    flat = foam_field.flatten()
    return entropy(flat)