# GRA-Living-Vaccine-Architecture

[Русский] | [English]

---

## Русский

### Самообучающаяся архитектура живых вакцин на принципах GRA

**Революционный фреймворк** для симуляции и проектирования программируемых терапевтических агентов (живых вакцин), способных адаптироваться к любым болезням благодаря иерархической стабильности, обнулению (nullification) и роевой координации. Основан на репозиториях GRA (Generalized Recursive Architecture).

> ⚠️ **Концептуальная платформа**: код предназначен для симуляций и исследований, не содержит инструкций по работе с реальными патогенами.

#### Основные возможности

- **DSL** для описания агентов (сигналы, состояния, правила, триггеры обнуления).
- **Симулятор** сигнальной среды (инфекция, воспаление, токсичность) с поддержкой роя.
- **Иерархическое обнуление**: жёсткое, мягкое, любовь-ориентированное (love‑oriented).
- **ИИ-дизайнер** на основе эволюционных стратегий для автоматической настройки правил.
- **Научная статья** (`paper.tex`) с формальным описанием архитектуры и экспериментов.

#### Быстрый старт

```bash
git clone https://github.com/ваш-аккаунт/GRA-Living-Vaccine-Architecture.git
cd GRA-Living-Vaccine-Architecture
python -m venv .venv
source .venv/bin/activate  # или .venv\Scripts\activate
pip install -r requirements.txt

# Базовый запуск симуляции
python sim/engine.py

# Эволюционный ИИ-дизайнер
python ai/designer.py
```

#### Структура

- `architecture/` — концептуальные документы (слои, протоколы обнуления).
- `dsl/` — схема языка и примеры агентов.
- `sim/` — движок симуляции, агенты, сигналы, рой.
- `ai/` — оптимизаторы и ИИ-дизайнер.
- `paper.tex` — научная статья (LaTeX).

#### Цитирование

Если вы используете эту архитектуру в исследованиях, ссылайтесь на `paper.tex` и оригинальные GRA-репозитории.

---

## English

### Self-Learning Vaccine Architecture based on GRA principles

**Revolutionary framework** for simulating and designing programmable therapeutic agents (living vaccines) that can adapt to any disease using hierarchical stability, nullification, and swarm coordination. Inspired by GRA (Generalized Recursive Architecture) repositories.

> ⚠️ **Conceptual platform**: code is for simulation and research only, no real pathogen handling instructions.

#### Key features

- **DSL** for agent specification (signals, states, rules, nullification triggers).
- **Signal environment simulator** (infection, inflammation, toxicity) with swarm support.
- **Hierarchical nullification**: hard, soft, love-oriented.
- **AI designer** based on evolutionary strategies for automatic rule tuning.
- **Scientific paper** (`paper.tex`) with formal architecture description and experiments.

#### Quick start

```bash
git clone https://github.com/your-account/GRA-Living-Vaccine-Architecture.git
cd GRA-Living-Vaccine-Architecture
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate
pip install -r requirements.txt

# Basic simulation
python sim/engine.py

# Evolutionary AI designer
python ai/designer.py
```

#### Structure

- `architecture/` — conceptual documents (layers, nullification protocols).
- `dsl/` — language schema and agent examples.
- `sim/` — simulation engine, agents, signals, swarm.
- `ai/` — optimizers and AI designer.
- `paper.tex` — scientific paper (LaTeX).

#### Citation

If you use this architecture in your research, please cite `paper.tex` and the original GRA repositories.
