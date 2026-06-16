"""
Basic proof-of-concept run for Immune GRA-Twin.

- Initializes ImmuneTwin with tumor cells and GRA-swarm agents.
- Runs simulation for N steps.
- Logs global Φ(t) over time.
- Plots Φ(t) curve to show foam suppression by the swarm.
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt

from .environment import ImmuneTwin


def run_sim(
    n_steps: int = 200,
    n_tumor: int = 50,
    n_scouts: int = 10,
    n_nullifiers: int = 20,
    n_memory: int = 5,
    seed: int | None = 42,
    save_csv: bool = True,
    out_dir: str | Path = "output",
):
    model = ImmuneTwin(
        n_tumor=n_tumor,
        n_scouts=n_scouts,
        n_nullifiers=n_nullifiers,
        n_memory=n_memory,
        seed=seed,
    )

    phi_history: list[float] = []

    for step in range(n_steps):
        model.step()
        phi_history.append(model.global_phi)
        if step % 20 == 0:
            print(f"Step {step:3d} | Φ = {model.global_phi:.4f}")

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if save_csv:
        csv_path = out_dir / "phi_history_basic.csv"
        with csv_path.open("w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["step", "phi"])
            for i, phi in enumerate(phi_history):
                writer.writerow([i, phi])
        print(f"[INFO] Saved Φ(t) history to {csv_path}")

    # Plot Φ(t)
    plt.figure(figsize=(8, 4))
    plt.plot(phi_history, label="Φ(t) with GRA-swarm")
    plt.xlabel("Step")
    plt.ylabel("Global Φ (foam)")
    plt.title("Foam suppression by Immune GRA-swarm (basic run)")
    plt.grid(True)
    plt.legend()
    png_path = out_dir / "phi_history_basic.png"
    plt.tight_layout()
    plt.savefig(png_path, dpi=150)
    print(f"[INFO] Saved Φ(t) plot to {png_path}")
    plt.show()


if __name__ == "__main__":
    run_sim()