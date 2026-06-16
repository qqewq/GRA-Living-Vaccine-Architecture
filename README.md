https://orcid.org/my-orcid?orcid=0009-0004-1872-1153
https://doi.org/10.5281/zenodo.20703591
------------------
# GRA-Living-Vaccine-Architecture

[Русский](#русский) | [English](#english)

---

## Русский

### Самообучающаяся архитектура живых вакцин на принципах GRA

**GRA-Living-Vaccine-Architecture** — это концептуальный и исследовательский фреймворк для симуляции и проектирования программируемых терапевтических агентов (живых вакцин).  
Архитектура использует принципы GRA (Generalized Recursive Architecture): иерархическая стабильность, обнуление (nullification) и роевую координацию.

> ⚠️ **Важно:** код предназначен только для симуляций и теоретических исследований.  
> Он не содержит инструкций по работе с реальными патогенами и не является медицинским продуктом.

---

### Ключевые идеи

- **Иерархическая стабильность:** состояние организма/среды разбито на уровни (сигналы, клетки, ткани, органы, поведенческий уровень), для каждого уровня есть свои критерии стабильности.
- **Обнуление (nullification):** целенаправленное подавление «пены» (foam) — хаотических, разрушительных паттернов (воспаление, токсический каскад и т.п.) через GRA-операторы.
- **Рой терапевтических агентов:** множество простых агентов, которые:
  - чувствуют сигналы среды,
  - обмениваются сообщениями,
  - принимают коллективные решения об обнулении.
- **Самообучение:** через DSL-конфигурации и ИИ‑дизайнер архитектура может адаптировать правила поведения роя под новую патологию.

Полное описание концепции см. в PDF:

- `GRA-Living-Vaccine-Architecture-ru.pdf`
- `GRA-Living-Vaccine-Architecture-en.pdf`

---

### Структура репозитория

```text
GRA-Living-Vaccine-Architecture/
├── architecture/                  # концептуальные документы (слои, протоколы обнуления, сценарии)
├── dsl/                           # язык описания агентов и среды (YAML/JSON схемы, примеры)
├── sim/                           # основной движок симуляции, модели сигналов, агентов и роя
├── ai/                            # ИИ-дизайнер, эволюционные/поисковые алгоритмы
├── examples/                      # примеры конфигураций и запусков симуляции
├── immune_twin/                   # Immune GRA-Twin: отдельный модуль верификации (Scout + Nullifier + Memory)
│   ├── environment.py             # среда, поле сигналов, расписание шагов
│   ├── agents.py                  # TumorCell, Scout, Nullifier, Memory
│   ├── foam.py                    # расчёт глобальной метрики Φ (foam-энтропия) и вспомогательные функции
│   ├── run.py                     # запуск симуляции и визуализация траектории Φ(t)
│   ├── requirements.txt           # зависимости для Mesa-прототипа
│   └── dsl_config.yaml            # пример DSL-описания роя для будущей интеграции
├── GRA-Living-Vaccine-Architecture-ru.pdf
├── GRA-Living-Vaccine-Architecture-en.pdf
├── paper-ru.tex                   # LaTeX-статья (русская версия)
├── paper.tex                      # LaTeX-статья (английская версия)
├── requirements.txt               # зависимости для основного кода
├── pyproject.toml                 # конфигурация пакета (если нужен pip/poetry)
├── LICENSE
└── README.md
```

---

### Быстрый старт (основная архитектура)

```bash
git clone https://github.com/qqewq/GRA-Living-Vaccine-Architecture.git
cd GRA-Living-Vaccine-Architecture

python -m venv .venv
source .venv/bin/activate        # Linux/macOS
# или
.\.venv\Scripts\activate         # Windows

pip install -r requirements.txt

# Базовый запуск симуляции (пример)
python sim/engine.py

# Пример запуска ИИ-дизайнера / оптимизатора правил
python ai/designer.py
```

Смотрите папку `examples/` для конкретных сценариев (подготовленные конфигурации и командные строки).

---

### Immune GRA-Twin (Scout + Nullifier + Memory)

Папка `immune_twin/` содержит минимально жизнеспособный прототип **Immune GRA‑Twin** на основе Mesa.  
Он используется как наглядный proof‑of‑concept:

- **TumorCell** — источники хаотического сигнала (foam).
- **Scout** — сканирует локальное поле, измеряет локальную энтропию и помечает зоны высокой пены.
- **Nullifier** — идёт по наводке скаута и подавляет foam локальными GRA‑операторами.
- **Memory** — запоминает зоны, где foam был подавлен, и усиливает ответ при рецидиве.

Цель: показать, что при скоординированной работе трёх ролей глобальная метрика Φ(t) (энтропия foam-поля) устойчиво падает к нулю, а без координации — нет.

#### Быстрый старт для Immune GRA‑Twin

```bash
cd immune_twin
pip install -r requirements.txt
python run.py
```

Вы увидите в логе значения Φ(t) и график динамики пены по шагам симуляции.

---

### Лицензия

Проект распространяется под лицензией MIT (см. файл `LICENSE`).  
Используйте, модифицируйте, форкайте и цитируйте свободно при указании авторства.

---

### Цитирование

Если вы используете эту архитектуру в исследованиях, пожалуйста:

- цитируйте `paper.tex` / `paper-ru.tex`,
- ссылайтесь на этот репозиторий и связанные GRA‑проекты (GRA-Core, GRA-Hierarchical-Stability и др.),
- при необходимости используйте DOI: `https://doi.org/10.5281/zenodo.20703591`.

---

## English

### Self-Learning Vaccine Architecture based on GRA principles

**GRA-Living-Vaccine-Architecture** is a conceptual and research framework for simulating and designing programmable therapeutic agents (living vaccines).  
The architecture is built on GRA (Generalized Recursive Architecture) principles: hierarchical stability, nullification, and swarm‑based coordination.

> ⚠️ **Important:** this code is intended for simulations and theoretical research only.  
> It does not contain any instructions for handling real pathogens and is not a medical product.

---

### Key ideas

- **Hierarchical stability:** the organism/environment state is decomposed into levels (signals, cells, tissues, organs, behavioral layer), each with its own stability criteria.
- **Nullification:** targeted suppression of “foam” — chaotic, destructive patterns (e.g., runaway inflammation, toxic cascades) via GRA operators.
- **Therapeutic agent swarm:** many simple agents that:
  - sense signals in the environment,
  - exchange messages,
  - make collective decisions about nullification.
- **Self-learning:** via DSL configurations and AI designers, the architecture can adapt agent rules to new pathologies.

For a full conceptual description see the PDFs:

- `GRA-Living-Vaccine-Architecture-en.pdf`
- `GRA-Living-Vaccine-Architecture-ru.pdf`

---

### Repository structure

```text
GRA-Living-Vaccine-Architecture/
├── architecture/                  # conceptual documents (layers, nullification protocols, scenarios)
├── dsl/                           # domain-specific language for agents and environment (schemas, examples)
├── sim/                           # main simulation engine, signal models, agents, and swarm logic
├── ai/                            # AI designer, evolutionary / search algorithms
├── examples/                      # example configurations and simulation run scripts
├── immune_twin/                   # Immune GRA-Twin: verification module (Scout + Nullifier + Memory, Mesa-based)
│   ├── environment.py
│   ├── agents.py
│   ├── foam.py
│   ├── run.py
│   ├── requirements.txt
│   └── dsl_config.yaml
├── GRA-Living-Vaccine-Architecture-en.pdf
├── GRA-Living-Vaccine-Architecture-ru.pdf
├── paper-ru.tex
├── paper.tex
├── requirements.txt
├── pyproject.toml
├── LICENSE
└── README.md
```

---

### Quick start (core architecture)

```bash
git clone https://github.com/qqewq/GRA-Living-Vaccine-Architecture.git
cd GRA-Living-Vaccine-Architecture

python -m venv .venv
source .venv/bin/activate        # Linux/macOS
# or
.\.venv\Scripts\activate         # Windows

pip install -r requirements.txt

# Basic simulation example
python sim/engine.py

# Evolutionary AI designer / rule optimizer
python ai/designer.py
```

See the `examples/` directory for ready‑made scenarios and command lines.

---

### Immune GRA-Twin (Scout + Nullifier + Memory)

The `immune_twin/` folder contains a minimal **Immune GRA‑Twin** proof‑of‑concept built on Mesa.  
It serves as a concrete verification module:

- **TumorCell** — sources of chaotic foam signal.
- **Scout** — scans the local field, measures local entropy, and marks high‑foam zones.
- **Nullifier** — moves towards Scout‑marked regions and locally suppresses foam via GRA operators.
- **Memory** — remembers previously suppressed regions and accelerates the response upon recurrence.

Goal: demonstrate that coordinated roles (Scout → Nullifier → Memory) drive the global foam entropy Φ(t) towards zero, whereas uncoordinated behavior does not.

#### Quick start for Immune GRA‑Twin

```bash
cd immune_twin
pip install -r requirements.txt
python run.py
```

This will print Φ(t) values to the console and display a plot of foam dynamics over simulation steps.

---

### License

This project is released under the MIT license (see `LICENSE`).  
You are free to use, modify, fork, and cite it with proper attribution.

---

### Citation

If you use this architecture or the Immune GRA‑Twin module in your research, please:

- cite `paper.tex` / `paper-ru.tex`,
- reference this repository and the related GRA projects (GRA‑Core, GRA‑Hierarchical‑Stability, etc.),
- optionally use the DOI: `https://doi.org/10.5281/zenodo.20703591`.
