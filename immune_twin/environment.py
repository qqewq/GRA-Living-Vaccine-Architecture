from mesa import Model
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation
from agents import TumorCell, Scout, Nullifier, Memory
from foam import compute_phi
import numpy as np

class ImmuneTwin(Model):
    def __init__(self, width=100, height=100, n_tumor=50, n_scouts=10,
                 n_nullifiers=20, n_memory=5):
        super().__init__()
        self.space = ContinuousSpace(width, height, torus=False)
        self.schedule = RandomActivation(self)
        self.width = width
        self.height = height

        # Создаём опухолевые клетки
        for _ in range(n_tumor):
            cell = TumorCell(self)
            x = self.random.uniform(0, width)
            y = self.random.uniform(0, height)
            self.space.place_agent(cell, (x, y))
            self.schedule.add(cell)

        # Создаём GRA‑агентов
        self.scouts = []
        for _ in range(n_scouts):
            scout = Scout(self)
            self.space.place_agent(scout, (self.random.uniform(0, width),
                                          self.random.uniform(0, height)))
            self.schedule.add(scout)
            self.scouts.append(scout)

        self.nullifiers = []
        for _ in range(n_nullifiers):
            nullifier = Nullifier(self)
            self.space.place_agent(nullifier, (self.random.uniform(0, width),
                                              self.random.uniform(0, height)))
            self.schedule.add(nullifier)
            self.nullifiers.append(nullifier)

        self.memories = []
        for _ in range(n_memory):
            mem = Memory(self)
            self.space.place_agent(mem, (self.random.uniform(0, width),
                                         self.random.uniform(0, height)))
            self.schedule.add(mem)
            self.memories.append(mem)

        # Поле "foam signal" – глобальная карта, обновляется каждый шаг
        self.foam_field = np.zeros((width, height))
        self.global_phi = 0.0

    def step(self):
        # 1. Опухолевые клетки излучают хаотический сигнал
        for agent in self.schedule.agents:
            if isinstance(agent, TumorCell):
                agent.emit_foam()
        # 2. Глобально вычисляем Φ
        self.global_phi = compute_phi(self.foam_field)
        # 3. Запускаем всех агентов (Scout, Nullifier, Memory)
        self.schedule.step()
