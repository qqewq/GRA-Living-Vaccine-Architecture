import numpy as np
from mesa import Agent
from foam import entropy

class TumorCell(Agent):
    def __init__(self, model):
        super().__init__(model)
        self.foam_strength = 10.0  # интенсивность хаоса

    def emit_foam(self):
        x, y = int(self.pos[0]), int(self.pos[1])
        # Каждая опухолевая клетка добавляет случайный шум в свою окрестность
        h = 3  # радиус влияния
        for dx in range(-h, h+1):
            for dy in range(-h, h+1):
                nx, ny = x+dx, y+dy
                if 0 <= nx < self.model.width and 0 <= ny < self.model.height:
                    self.model.foam_field[nx, ny] += np.random.normal(0, self.foam_strength/5)

class Scout(Agent):
    def __init__(self, model):
        super().__init__(model)
        self.detection_radius = 10

    def step(self):
        # Сканируем локальную область и вычисляем локальную Φ
        x, y = int(self.pos[0]), int(self.pos[1])
        r = self.detection_radius
        local_field = self.model.foam_field[max(0,x-r):min(self.model.width, x+r),
                                            max(0,y-r):min(self.model.height, y+r)]
        if local_field.size > 0:
            local_phi = entropy(local_field.flatten())
        else:
            local_phi = 0
        # Если локальный foam высок, «помечаем» ближайшего Nullifier'а
        if local_phi > 2.0:  # порог
            for agent in self.model.nullifiers:
                if not agent.target:  # свободен
                    agent.target = (x, y)
                    agent.mode = "suppress"
                    break

class Nullifier(Agent):
    def __init__(self, model):
        super().__init__(model)
        self.target = None
        self.mode = "idle"

    def step(self):
        if self.mode == "suppress" and self.target:
            tx, ty = self.target
            # Двигаемся к цели
            dx = tx - self.pos[0]
            dy = ty - self.pos[1]
            step_size = 2.0
            dist = np.sqrt(dx**2 + dy**2)
            if dist > 1:
                self.model.space.move_agent(self, (self.pos[0] + dx/dist * step_size,
                                                   self.pos[1] + dy/dist * step_size))
            # Применяем GRA‑оператор: локально гасим foam
            x, y = int(self.pos[0]), int(self.pos[1])
            r = 3
            for i in range(max(0,x-r), min(self.model.width, x+r+1)):
                for j in range(max(0,y-r), min(self.model.height, y+r+1)):
                    self.model.foam_field[i,j] *= 0.2  # подавление
            # Если foam в целевой точке стал мал, завершаем
            if self.model.foam_field[tx, ty] < 0.5:
                self.target = None
                self.mode = "idle"
                # Активируем Memory
                for mem in self.model.memories:
                    mem.record(self.pos)

class Memory(Agent):
    def __init__(self, model):
        super().__init__(model)
        self.memory_map = np.zeros((model.width, model.height))

    def record(self, pos):
        x, y = int(pos[0]), int(pos[1])
        r = 5
        for i in range(max(0,x-r), min(self.model.width, x+r+1)):
            for j in range(max(0,y-r), min(self.model.height, y+r+1)):
                self.memory_map[i,j] = 1

    def step(self):
        # Если в зоне памяти снова появляется foam, немедленно вызываем Nullifier'а
        x, y = int(self.pos[0]), int(self.pos[1])
        if self.memory_map[x,y] > 0 and self.model.foam_field[x,y] > 2.0:
            for agent in self.model.nullifiers:
                if not agent.target:
                    agent.target = (x, y)
                    agent.mode = "suppress"
                    break
