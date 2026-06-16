from environment import ImmuneTwin
import matplotlib.pyplot as plt
import numpy as np

model = ImmuneTwin(n_tumor=50, n_scouts=10, n_nullifiers=20, n_memory=5)
phi_history = []

for i in range(200):
    model.step()
    phi_history.append(model.global_phi)
    if i % 20 == 0:
        print(f"Step {i}, Φ = {model.global_phi:.3f}")

plt.plot(phi_history)
plt.xlabel("Шаг")
plt.ylabel("Глобальная Φ (foam)")
plt.title("Динамика подавления foam GRA‑роем")
plt.grid()
plt.show()
