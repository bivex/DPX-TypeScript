<div align="center">

<h1>🔷 DPX-TypeScript</h1>

<p><strong>Hexagonal Architecture Pattern Detector & IDE Observability HUD<br>for TypeScript, JavaScript, React, Next.js, Node.js</strong></p>

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6.svg?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES2022+-F7DF1E.svg?logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![GoF: 23/23](https://img.shields.io/badge/GoF-23%2F23%20Patterns-blueviolet.svg)](https://en.wikipedia.org/wiki/Design_Patterns)
[![Rules: 40](https://img.shields.io/badge/Rules-40%20Detection%20Rules-cyan.svg)](#-40-detection-rules)
[![Architecture: Hexagonal DDD](https://img.shields.io/badge/Architecture-Hexagonal%20Ports%20%26%20Adapters-purple.svg)](https://en.wikipedia.org/wiki/Hexagonal_architecture_(software))
[![Tests](https://img.shields.io/badge/Tests-14%2F14%20Passing-35D07F.svg)](#-running-tests)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

</div>

---

**DPX-TypeScript** is a zero-dependency static architecture analysis engine for **TypeScript and JavaScript** codebases. It detects design patterns, type safety hazards, async race conditions, and SOLID violations — generating a beautiful IDE-like **Architecture Observability HUD** report.

Built with **Hexagonal Architecture (Ports & Adapters)** and **Domain-Driven Design**, DPX-TypeScript uses a native regex/AST parser — **no `tsc`, no `node_modules`, no build step required**.

---

## 🚀 Key Features

- **⚡ Zero-dependency native parser** — scans `.ts`, `.tsx`, `.js`, `.jsx`, `.mts`, `.cts` files with no compiler needed
- **🔷 40 detection rules** — full **GoF 23/23** + TypeScript idioms, async safety, and quality principles  
- **🖥️ IDE Architecture HUD** — 3-pane dark dashboard (Navigator · Findings Stream · Inspector Drawer) with density switcher, module hotspot matrix, and one-click AI prompt export
- **🤖 AI Architect Actions** — generates inline review / refactoring / explanation prompts for Claude, ChatGPT, Gemini
- **📁 Directory exclusions** — auto-skips `node_modules`, `dist`, `.next`, `coverage`, `.docusaurus`

---

## 🎯 40 Detection Rules

```
                    🔷 DPX-TypeScript Pattern & Architecture Matrix
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Category                     ┃ Rule Identifier                    ┃ TypeScript Idiom / Pattern                ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 1. Type-Level Programming    │ discriminated_union                │ type Shape = Circle | Square (kind tag)   │
│    (5 rules)                 │ conditional_types                  │ T extends Promise<infer U> ? U : T        │
│                              │ mapped_types                       │ { [P in keyof T]: T[P] | null }           │
│                              │ branded_types                      │ string & { __brand: 'UserId' }            │
│                              │ type_guard_predicate               │ fn(x): x is Circle { ... }                │
├──────────────────────────────┼────────────────────────────────────┼───────────────────────────────────────────┤
│ 2. Creational GoF            │ builder_pattern                    │ new QueryBuilder().where().limit().build()│
│    (5 rules · GoF ✅)        │ abstract_factory          ★ GoF   │ interface UIFactory { createBtn(): Btn }  │
│                              │ factory_method                     │ static create(): Result<T, E>             │
│                              │ singleton_pattern                  │ private static instance; getInstance()    │
│                              │ prototype_clone                    │ structuredClone(obj) / clone pattern      │
├──────────────────────────────┼────────────────────────────────────┼───────────────────────────────────────────┤
│ 3. Structural GoF            │ adapter_pattern                    │ class TSAdapter implements LegacyPort     │
│    (7 rules · GoF ✅)        │ bridge_pattern            ★ GoF   │ abstract Remote(protected device: Device) │
│                              │ composite_pattern         ★ GoF   │ Directory.children: FileSystemItem[]      │
│                              │ decorator_pattern                  │ @Injectable() / @Controller() AOP         │
│                              │ facade_pattern                     │ class ApiClient wrapping N services       │
│                              │ flyweight_pattern         ★ GoF   │ private cache = new Map<K,V>()            │
│                              │ proxy_handler                      │ new Proxy(target, { get, set })           │
├──────────────────────────────┼────────────────────────────────────┼───────────────────────────────────────────┤
│ 4. Behavioral GoF            │ observer_event_emitter             │ extends EventEmitter / RxJS Observable    │
│    (11 rules · GoF ✅)       │ strategy_pattern                   │ interface SortStrategy { sort(arr) }      │
│                              │ chain_of_responsibility            │ async (ctx, next) => { await next() }     │
│                              │ command_pattern                    │ class CreateUserCommand { execute() }     │
│                              │ async_iterator_generator           │ async function* streamResults()           │
│                              │ template_method           ★ GoF   │ abstract class Miner { mine() { ... } }   │
│                              │ state_pattern             ★ GoF   │ type Light = 'red'|'green'|'yellow' FSM   │
│                              │ visitor_pattern           ★ GoF   │ interface Visitor { visitLiteral(n) }     │
│                              │ mediator_pattern          ★ GoF   │ class EventBus { on/emit/off }            │
│                              │ memento_pattern           ★ GoF   │ history.push({...state}) / undo stack     │
│                              │ interpreter_pattern       ★ GoF   │ interface Expr { interpret(ctx): number } │
├──────────────────────────────┼────────────────────────────────────┼───────────────────────────────────────────┤
│ 5. Architectural             │ dependency_injection               │ @Inject('TOKEN') constructor(svc: Svc)    │
│    (4 rules)                 │ repository_pattern                 │ interface UserRepo { findById(id) }       │
│                              │ railway_result_monad               │ type Result<T,E> = Ok<T> | Err<E>         │
│                              │ smart_constructor                  │ class Email { static create(): Result }   │
├──────────────────────────────┼────────────────────────────────────┼───────────────────────────────────────────┤
│ 6. Concurrency & Async       │ structured_promise_all             │ Promise.allSettled([...]) coordination    │
│    (4 rules)                 │ unhandled_promise_rejection        │ floating .then() without .catch()         │
│                              │ async_race_condition               │ shared mutable state across await points  │
│                              │ abort_controller_cancellation      │ new AbortController() / signal propagation│
├──────────────────────────────┼────────────────────────────────────┼───────────────────────────────────────────┤
│ 7. Resilience & Hazards 🔴   │ unsafe_any_assertion               │ payload as any — bypasses type safety     │
│    (4 rules)                 │ unsafe_non_null_assertion          │ value! — runtime NPE risk                 │
│                              │ try_catch_blanket_swallow          │ catch (e) {} — silent failure             │
│                              │ mutable_global_state               │ export let session = null — race hazard   │
├──────────────────────────────┼────────────────────────────────────┼───────────────────────────────────────────┤
│ 8. Quality & Principles ⚖️   │ god_module_srp                     │ >400 LOC single-responsibility violation  │
│    (4 rules)                 │ cyclomatic_complexity_kiss         │ >10 branches — KISS violation             │
│                              │ duplicate_code_dry                 │ repeated logic blocks — DRY violation     │
│                              │ circular_module_import             │ A→B→A import cycle — undefined at runtime │
└──────────────────────────────┴────────────────────────────────────┴───────────────────────────────────────────┘
```

> ★ GoF = newly added to complete full Gang of Four coverage

---

## ⚡ Benchmarks on Real-World TypeScript Projects

| Project | Files | Findings | Scan Time |
|---|:---:|:---:|:---:|
| `examples/ts_samples` (BankingDomain · ApiGateway · GoFPatterns) | **3** | **89** | **< 0.1s** |

---

## 🛠️ Installation & Usage

```bash
# Clone
git clone https://github.com/bivex/DPX-TypeScript.git
cd DPX-TypeScript

# Install (uv recommended)
uv pip install -e ".[dev]"
# or pip
pip install -e ".[dev]"
```

```bash
# Scan a TypeScript/JavaScript project
dpx-ts ./src

# Generate IDE Architecture HUD report
dpx-ts ./src -H reports/report.html

# Exclude directories
dpx-ts ./src -e dist -e __tests__ -e node_modules -H reports/report.html

# Verbose — show all findings
dpx-ts ./src -v
```

---

## 🖥️ IDE Architecture Observability HUD

The HTML report is a fully interactive 3-pane dashboard — no server, no framework, pure HTML + JS:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│  TS  DPX Architecture HUD   my-project   TypeScript Observability Engine               │
│  📁 3 files  ⏱ 0.09s  🔷 89 findings  🔴 2 action required          [AI Context] [💾] │
├──── ARCHITECTURE HEALTH: ████████████████░░  92% ──────────────────────────────────────┤
├──────────────────┬──────────────────────────────────────────┬──────────────────────────┤
│ ARCHITECTURE NAV │ FINDINGS STREAM           [Density ▾] 🔍 │ INSPECTOR DRAWER         │
│                  │                                          │                          │
│ Views            │ #1  visitor_pattern         ★ GoF        │ #1  visitor_pattern      │
│ 📋 Findings  89  │ GoFPatterns.ASTVisitor                   │ GoFPatterns · Structural │
│ 🗺️ Hotspots   3  │ 📍 GoFPatterns.ts:98:1  •  90% VERY HIGH│                          │
│                  │ ─────────────────────────────────────── │ IMPACT: HIGH             │
│ FILTER           │ #2  template_method         ★ GoF        │ CONF:   90% [VERY HIGH]  │
│ ◉ All        89  │ GoFPatterns.DataMiner                    │                          │
│ 🔴 Action     2  │ 📍 GoFPatterns.ts:67:1  •  85% VERY HIGH│ EVIDENCE TRAIL           │
│ 🔷 Type Sys   9  │ ─────────────────────────────────────── │ +90% VISITOR_INTERFACE   │
│ 🟢 Creational 19 │ #3  abstract_factory        ★ GoF        │ Interface 'ASTVisitor'   │
│ 🟣 Structural 36 │ GoFPatterns.UIFactory                    │ declares 3 visit*()      │
│ 🟠 Behavioral 15 │ 📍 GoFPatterns.ts:4:1   •  85% VERY HIGH│ methods                  │
│ ⚡ Async      5  │                                          │                          │
│                  │                                          │ AI ARCHITECT ACTIONS     │
│ MODULE HOTSPOTS  │                                          │ [💡 Review]              │
│ ● GoFPatterns 47 │                                          │ [🛠️ Refactor]            │
│ ● BankingDomain  │                                          │ [🔍 Explain]             │
└──────────────────┴──────────────────────────────────────────┴──────────────────────────┘
```

**Features:**
- 🔍 **Live search** across all findings
- 📐 **Density switcher** — Comfortable / Compact view
- 🗺️ **Module Hotspots matrix** — see which files concentrate the most signals
- 🤖 **AI Context export** — one-click LLM-optimized architectural prompt
- 💡 **Inspector Drawer** — Evidence trail, confidence score, source location
- 💾 **JSON export** — all findings as structured data

---

## 🏗️ Architecture

```
src/pattern_detector/
├── domain/
│   ├── value_objects.py              # PatternCategory (8), PatternType (40), Confidence
│   ├── code_model.py                 # TSModule, TSClass, TSInterface, TSTypeAlias, TSFunction
│   ├── detection.py                  # Detection, DetectionReport (Pydantic)
│   ├── pattern.py                    # 40 PatternCatalogEntry with descriptions & examples
│   └── rules/
│       ├── type_programming_rules.py # 5 rules — Discriminated Union, Conditional, Mapped, Branded, Guard
│       ├── creational_rules.py       # 4 rules — Builder, Factory Method, Singleton, Prototype
│       ├── structural_rules.py       # 4 rules — Adapter, Decorator, Facade, Proxy
│       ├── behavioral_rules.py       # 5 rules — Observer, Strategy, Chain, Command, AsyncIterator
│       ├── enterprise_rules.py       # 4 rules — DI, Repository, Railway, SmartConstructor
│       ├── async_concurrency_rules.py# 4 rules — PromiseAll, Floating, RaceCondition, AbortController
│       ├── resilience_rules.py       # 4 rules — UnsafeAny, NonNull, EmptyCatch, MutableGlobal
│       ├── quality_rules.py          # 4 rules — GodModule, Complexity, DRY, CircularImport
│       ├── gof_missing_rules.py      # 10 rules — AbstractFactory, Bridge, Composite, Flyweight,
│       │                             #            TemplateMethod, State, Visitor, Mediator, Memento, Interpreter
│       └── __init__.py               # DEFAULT_RULES — all 40 rules registered
├── application/
│   └── detection_service.py          # DetectionService — orchestrator
├── adapters/
│   ├── inbound/cli/main.py           # CLI entrypoint (Typer + Rich)
│   └── outbound/
│       ├── parsers/
│       │   └── native_ts_parser_adapter.py  # Zero-dependency regex/AST parser
│       └── persistence/
│           └── html_report_formatter.py     # IDE Architecture HUD generator
└── ports/
    ├── inbound.py                    # ScanProjectUseCase protocol
    └── outbound.py                   # ReportFormatterPort, ResultRepositoryPort
```

---

## ✅ Gang of Four: 23/23 Complete

| | Creational (5/5) | Structural (7/7) | Behavioral (11/11) |
|---|---|---|---|
| ✅ | Abstract Factory | Adapter | Chain of Responsibility |
| ✅ | Builder | Bridge | Command |
| ✅ | Factory Method | Composite | Interpreter |
| ✅ | Prototype | Decorator | Iterator (Async) |
| ✅ | Singleton | Facade | Mediator |
| ✅ | | Flyweight | Memento |
| ✅ | | Proxy | Observer |
| ✅ | | | State |
| ✅ | | | Strategy |
| ✅ | | | Template Method |
| ✅ | | | Visitor |

---

## 🧪 Running Tests

```bash
uv run pytest tests/ -v
```

```
tests/test_detection_service.py::test_scan_examples          PASSED
tests/test_detection_service.py::test_scan_summary_by_category PASSED
tests/test_detection_service.py::test_scan_produces_html     PASSED
tests/test_parser.py::test_parse_examples                    PASSED
tests/test_parser.py::test_parse_detects_classes             PASSED
tests/test_parser.py::test_parse_detects_type_aliases        PASSED
tests/test_resilience_rules.py::test_unsafe_any_detected     PASSED
tests/test_resilience_rules.py::test_non_null_assertion_detected PASSED
tests/test_resilience_rules.py::test_empty_catch_detected    PASSED
tests/test_resilience_rules.py::test_mutable_global_detected PASSED
tests/test_type_programming_rules.py::test_discriminated_union_detected PASSED
tests/test_type_programming_rules.py::test_conditional_type_detected PASSED
tests/test_type_programming_rules.py::test_mapped_type_detected PASSED
tests/test_type_programming_rules.py::test_branded_type_detected PASSED

14 passed in 0.09s
```

---

## 📁 Supported File Types

| Extension | Description |
|---|---|
| `.ts` | TypeScript source |
| `.tsx` | TypeScript + JSX (React) |
| `.js` | JavaScript (ES2022+) |
| `.jsx` | JavaScript + JSX |
| `.mts` / `.cts` | TypeScript ES Modules / CommonJS |

**Auto-excluded:** `node_modules/` · `dist/` · `build/` · `.next/` · `coverage/` · `.docusaurus/` · `*.d.ts`

---

## 🌐 DPX Suite

DPX-TypeScript is part of the **DPX (Design Patterns X)** multi-language architecture scanner family:

| Repo | Language | Rules |
|---|---|---|
| [DPX-Haskell](https://github.com/bivex/DPX-Haskell) | Haskell / GHC 9.x | 26 |
| [DPX-TypeScript](https://github.com/bivex/DPX-TypeScript) | TypeScript / JavaScript | **40** |
| [DPX-Rust](https://github.com/bivex/DPX-Rust) | Rust 2015–2024 | 41 |
| [DPX-Go](https://github.com/bivex/DPX-Go) | Go 1.18–1.24 | — |
| [DPX-Py](https://github.com/bivex/DPX-Py) | Python 3.8–3.13 | — |
| [DPX-Php](https://github.com/bivex/DPX-Php) | PHP 7.4–8.4 | 23 |
| [DPX-Elixir](https://github.com/bivex/DPX-Elixir) | Elixir / OTP | — |
| [DPX-Erlang](https://github.com/bivex/DPX-Erlang) | Erlang / OTP | — |
| [DPX-C](https://github.com/bivex/DPX-C) | C89 / C99 / C11 / C17 / C23 | — |
| [DPX-OCaml](https://github.com/bivex/DPX-OCaml) | OCaml 4.14–5.3+ | — |

---

## 📄 License

MIT © [bivex](https://github.com/bivex)
