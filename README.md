<div align="center">

# 🔷 DPX-TypeScript

**Multi-Paradigm Hexagonal Architecture & Design Pattern Scanner for TypeScript / JavaScript**

*Detects 40 architectural patterns, all 23 Gang of Four (GoF) patterns, type-level programming idioms, async concurrency hazards, and SOLID smells — complete with an interactive IDE-like Observability HUD.*

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![TypeScript Support](https://img.shields.io/badge/TypeScript-5.x%20%2F%20ES2022%2B-3178C6.svg?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![GoF Coverage](https://img.shields.io/badge/GoF%20Patterns-23%2F23%20(100%25)-8A2BE2.svg)](https://en.wikipedia.org/wiki/Design_Patterns)
[![Detection Rules](https://img.shields.io/badge/Rules-40%20Detection%20Rules-00D8FF.svg)](#-catalog-of-40-detection-rules)
[![Architecture](https://img.shields.io/badge/Architecture-Hexagonal%20DDD-9333EA.svg)](https://en.wikipedia.org/wiki/Hexagonal_architecture_(software))
[![Tests Passing](https://img.shields.io/badge/Tests-14%2F14%20Passing-35D07F.svg)](#-test-suite)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

[**Quick Start**](#-quick-start) •
[**Pattern Catalog**](#-catalog-of-40-detection-rules) •
[**Architecture HUD**](#-architecture-observability-hud) •
[**Benchmarks**](#-real-world-benchmarks) •
[**CLI Reference**](#-cli-commands)

</div>

---

## 💡 Overview

**DPX-TypeScript** is a deterministic static analyzer designed specifically for modern TypeScript and JavaScript codebases (React, Next.js, Node.js, NestJS, Deno, Bun).

Unlike general-purpose linters, DPX-TypeScript operates at the **architectural abstraction level**:
- **Zero-Dependency Native Parser:** Parses `.ts`, `.tsx`, `.js`, `.jsx`, `.mts`, `.cts` files instantly without needing `tsc`, `tsconfig.json`, or heavy `node_modules`.
- **Complete GoF 23/23 Coverage:** Classifies all classical creational, structural, and behavioral design patterns.
- **Deep Type-Level Analysis:** Identifies Discriminated Unions, Branded Nominal Types, Mapped/Conditional Types, and Type Guard Predicates.
- **Async Concurrency & Hazard Guard:** Pinpoints floating unhandled promises, state race conditions across `await` points, blanket try/catch swallowing, and unsafe `as any` casts.
- **IDE Architecture Observability HUD:** Generates an interactive, standalone HTML dashboard with source navigation, metric hotspots, and one-click AI architectural review prompts.

---

## ⚡ Real-World Benchmarks

Tested against large open-source codebases cloned directly from GitHub:

| Repository | Focus Area | Files Scanned | Findings | Scan Time | Top Architectural Signals |
|---|---|:---:|:---:|:---:|---|
| [**honojs/hono**](https://github.com/honojs/hono) | Web Framework | 310 | 360 | **0.28s** | `chain_of_responsibility` (59), `mapped_types` (23), `async_race_condition` (25) |
| [**colinhacks/zod**](https://github.com/colinhacks/zod) | Schema & Types | 321 | 464 | **0.22s** | `conditional_types` (78), `mapped_types` (55), `unsafe_any_assertion` (84) |
| [**examples/ts_samples**](./examples/ts_samples) | GoF + Enterprise | 3 | 89 | **0.01s** | Complete GoF 23/23 patterns, Smart Constructors, Railway Result |
| **TOTAL** | | **634** | **913** | **0.51s** | **~1,800 files/sec throughput** |

---

## 🚀 Quick Start

### 1. Installation

```bash
# Using uv (fastest)
uv pip install -e ".[dev]"

# Or standard pip
pip install -e ".[dev]"
```

### 2. Basic Scan

```bash
# Scan directory with terminal summary
dpx-ts scan ./src

# Scan and output interactive HTML Architecture HUD
dpx-ts scan ./src -H reports/architecture_hud.html

# Exclude build artifacts and vendor dirs
dpx-ts scan ./src -e dist -e node_modules -e coverage -H reports/hud.html
```

---

## 🎯 Catalog of 40 Detection Rules

<details open>
<summary><b>1. Type-Level Programming & Generics (5 Rules)</b></summary>
<br>

| Rule Identifier | Description | Idiomatic TypeScript Pattern |
|---|---|---|
| `discriminated_union` | Tagged / Discriminated Union modeling algebraic data types | `type Action = { type: 'inc' } \| { type: 'dec' }` |
| `conditional_types` | Non-trivial type-level computation and inference | `type Unbox<T> = T extends Promise<infer U> ? U : T` |
| `mapped_types` | Homogeneous object transformations and key mapping | `type Nullable<T> = { [P in keyof T]: T[P] \| null }` |
| `branded_types` | Nominal type tagging preventing primitive obsession | `type UserId = string & { readonly __brand: 'UserId' }` |
| `type_guard_predicate` | Custom boolean type guard or assertion predicate | `function isUser(v: unknown): v is User { ... }` |

</details>

<details open>
<summary><b>2. Creational Patterns — Full GoF (5 Rules)</b></summary>
<br>

| Rule Identifier | GoF | Description | Idiomatic TypeScript Pattern |
|---|:---:|---|---|
| `builder_pattern` | ✅ | Fluent chained method object construction | `new QueryBuilder().where(...).limit(...).build()` |
| `abstract_factory` | ✅ | Families of related object creation interfaces | `interface UIFactory { createButton(): Button; createDialog(): Dialog; }` |
| `factory_method` | ✅ | Factory methods delegating instance creation | `static create(): Result<T, Error>` |
| `singleton_pattern` | ✅ | Single shared instance with private constructor | `private static instance; static getInstance()` |
| `prototype_clone` | ✅ | Deep/shallow cloning of prototypical objects | `structuredClone(state)` / prototype delegation |

</details>

<details open>
<summary><b>3. Structural Patterns — Full GoF (7 Rules)</b></summary>
<br>

| Rule Identifier | GoF | Description | Idiomatic TypeScript Pattern |
|---|:---:|---|---|
| `adapter_pattern` | ✅ | Wrapper converting incompatible interfaces | `class ExpressAdapter implements HttpHandler { ... }` |
| `bridge_pattern` | ✅ | Decouples abstraction from implementation via composition | `abstract class Remote { constructor(protected dev: Device) {} }` |
| `composite_pattern` | ✅ | Recursive tree structure treating parts and wholes uniformly | `interface Node { size(): number; children: Node[]; }` |
| `decorator_pattern` | ✅ | Metaprogramming and aspect-oriented annotations | `@Injectable()`, `@Controller()`, `@UseGuards()` |
| `facade_pattern` | ✅ | Simplified high-level facade interface over subsystems | `class ApiFacade { constructor(private auth, private billing) {} }` |
| `flyweight_pattern` | ✅ | Shared object pool reducing memory footprint | `private cache = new Map<string, Glyph>(); get(k)` |
| `proxy_handler` | ✅ | Trap interception and reactive proxies | `new Proxy(target, { get, set, apply })` |

</details>

<details open>
<summary><b>4. Behavioral & Reactive Patterns — Full GoF (11 Rules)</b></summary>
<br>

| Rule Identifier | GoF | Description | Idiomatic TypeScript Pattern |
|---|:---:|---|---|
| `observer_event_emitter` | ✅ | Pub/Sub subscriber notification | `class Bus extends EventEmitter`, RxJS `Subject` |
| `strategy_pattern` | ✅ | Interchangeable pluggable algorithmic strategies | `interface SortStrategy { sort(items: T[]): T[]; }` |
| `chain_of_responsibility` | ✅ | Pipeline execution of middleware handlers | `async (ctx: Context, next: Next) => { await next(); }` |
| `command_pattern` | ✅ | Encapsulated executable action objects | `class CreateOrderCommand { execute(): Promise<void> }` |
| `async_iterator_generator` | ✅ | Asynchronous iteration over data streams | `async function* streamBatches(): AsyncGenerator<T>` |
| `template_method` | ✅ | Skeleton algorithm deferring steps to subclasses | `abstract class Miner { mine() { extract(); parse(); } }` |
| `state_pattern` | ✅ | Finite state machine altering object behaviour | `type State = 'idle' \| 'loading' \| 'error'` transitions |
| `visitor_pattern` | ✅ | Double-dispatch separating operations from AST structures | `interface ASTVisitor { visitBinary(node); visitLiteral(node); }` |
| `mediator_pattern` | ✅ | Centralized communication broker decoupling components | `class EventBus { on(e, fn); emit(e, data); }` |
| `memento_pattern` | ✅ | State snapshot capture supporting undo/rollback | `history.push({ ...state }); restore(history.pop());` |
| `interpreter_pattern` | ✅ | Expression tree evaluation and DSL execution | `interface Expr { interpret(ctx: Context): number; }` |

</details>

<details open>
<summary><b>5. Architectural & Enterprise Patterns (4 Rules)</b></summary>
<br>

| Rule Identifier | Description | Idiomatic TypeScript Pattern |
|---|---|---|
| `dependency_injection` | Inversion of Control container and token injection | `@Inject('USER_SERVICE') private readonly svc` |
| `repository_pattern` | Domain storage boundary decoupling persistence | `interface UserRepository { findById(id): Promise<User>; }` |
| `railway_result_monad` | Functional error handling with total explicit Result | `type Result<T, E> = { ok: true; val: T } \| { ok: false; err: E }` |
| `smart_constructor` | Value object validation enforcing domain invariants | `class Email { private constructor(); static create(raw): Result; }` |

</details>

<details open>
<summary><b>6. Concurrency, Async Safety & Streams (4 Rules)</b></summary>
<br>

| Rule Identifier | Risk Level | Description | Idiomatic TypeScript Pattern |
|---|:---:|---|---|
| `structured_promise_all` | Info | Safe structured concurrent execution | `Promise.allSettled([fetchA(), fetchB()])` |
| `unhandled_promise_rejection` | ⚠️ Warning | Floating promise without await or catch handler | `fetchData();` (missing `.catch()` or `await`) |
| `async_race_condition` | 🔴 Hazard | Mutable shared state mutated across async checkpoints | Modifying class fields before and after `await` |
| `abort_controller_cancellation` | Safe | Cooperative async task cancellation | `const ctrl = new AbortController(); fetch(url, { signal })` |

</details>

<details open>
<summary><b>7. Resilience & Type Safety Hazards (4 Rules)</b></summary>
<br>

| Rule Identifier | Severity | Description | Anti-Pattern |
|---|:---:|---|---|
| `unsafe_any_assertion` | 🔴 High | Bypassing type safety via escape-hatch `as any` | `const data = (response as any).data` |
| `unsafe_non_null_assertion` | ⚠️ Medium | Runtime Null Pointer risk via `!` operator | `const el = document.getElementById('app')!` |
| `try_catch_blanket_swallow` | 🔴 High | Swallowing errors silently in empty catch blocks | `try { ... } catch (err) {}` |
| `mutable_global_state` | ⚠️ Medium | Global mutable variable exports causing state leaks | `export let currentSession: Session \| null = null;` |

</details>

<details open>
<summary><b>8. Principles & Code Quality (4 Rules)</b></summary>
<br>

| Rule Identifier | Principle | Threshold | Description |
|---|:---:|:---:|---|
| `god_module_srp` | Single Responsibility (SRP) | > 400 LOC | Overly coupled god-module centralising too many responsibilities |
| `cyclomatic_complexity_kiss` | Keep It Simple (KISS) | > 10 Branches | High nesting and complex branching density |
| `duplicate_code_dry` | Don't Repeat Yourself (DRY) | Repeated blocks | Duplicated logic across independent functions |
| `circular_module_import` | Clean Dependency Graph | Import Cycle | Cyclic dependencies causing `undefined` at module load time |

</details>

---

## 🖥️ Architecture Observability HUD

When run with `-H output.html`, DPX-TypeScript produces a standalone, zero-dependency IDE Architecture Dashboard:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│  TS  DPX Architecture HUD   my-project   TypeScript Observability Engine               │
│  📁 310 files  ⏱ 0.28s  🔷 360 findings  🔴 62 action required      [AI Context] [💾] │
├──── ARCHITECTURE HEALTH: ████████████████░░  88% ──────────────────────────────────────┤
├──────────────────┬──────────────────────────────────────────┬──────────────────────────┤
│ ARCHITECTURE NAV │ FINDINGS STREAM           [Density ▾] 🔍 │ INSPECTOR DRAWER         │
│                  │                                          │                          │
│ Views            │ #1  chain_of_responsibility              │ #1  chain_of_responsibility
│ 📋 Findings  360 │ hono.HonoBase.use                        │ hono.HonoBase · Behavioral│
│ 🗺️ Hotspots   12 │ 📍 src/hono-base.ts:142:1  • 95% VERY HIGH│                         │
│                  │ ─────────────────────────────────────── │ IMPACT: HIGH             │
│ FILTER           │ #2  mapped_types                         │ CONF:   95% [VERY HIGH]  │
│ ◉ All        360 │ context.HeaderRecord                     │                          │
│ 🔴 Action     62 │ 📍 src/context.ts:17:1     • 95% VERY HIGH│ EVIDENCE TRAIL           │
│ 🔷 Type Sys   57 │ ─────────────────────────────────────── │ +85% MAPPED_HOMOGENEOUS  │
│ 🟢 Creational 20 │ #3  async_race_condition         🔴      │ Type alias HeaderRecord  │
│ 🟣 Structural 42 │ request.HonoRequest.parse                │ implements Mapped Types  │
│ 🟠 Behavioral 63 │ 📍 src/request.ts:65:1     • 85% HIGH    │ for key transformation   │
│ ⚡ Async      41 │                                          │                          │
│                  │                                          │ AI ARCHITECT ACTIONS     │
│ MODULE HOTSPOTS  │                                          │ [💡 Review Architecture] │
│ ● hono-base   48 │                                          │ [🛠️ Refactor Pattern]   │
│ ● context     32 │                                          │ [🔍 Explain Finding]     │
└──────────────────┴──────────────────────────────────────────┴──────────────────────────┘
```

### Key HUD Capabilities:
- **3-Pane IDE Layout:** File Navigator on the left, live Findings Stream in the center, and deep Inspector Drawer on the right.
- **Evidence Trail:** Every detection includes confidence heuristics and rule weights.
- **Module Hotspots Matrix:** Aggregates architectural density by source file.
- **AI Context Integration:** One-click generation of structured prompts for Claude, ChatGPT, or Gemini to review or refactor the finding.

---

## 🛠️ CLI Commands

```bash
# 1. Scan a project directory or file
dpx-ts scan <path> [OPTIONS]

Options:
  -H, --html <path>     Export interactive HTML Architecture HUD report
  -e, --exclude <dir>   Exclude directory from scan (repeatable)
  -v, --verbose         Output full detection details to console
  --help                Show command help

# 2. View all 40 registered rules with descriptions
dpx-ts rules

# 3. Check CLI version
dpx-ts version
```

---

## 🏛️ Hexagonal Architecture Design

DPX-TypeScript is structured using strict **Hexagonal Architecture (Ports & Adapters)**:

```
src/pattern_detector/
├── domain/                          # Core Domain Logic (No external dependencies)
│   ├── value_objects.py             # PatternCategory, PatternType, Confidence
│   ├── code_model.py                # AST abstractions (TSModule, TSClass, TSInterface, etc.)
│   ├── detection.py                 # Detection and DetectionReport domain models
│   ├── pattern.py                   # Catalog metadata for all 40 patterns
│   └── rules/                       # 40 decoupled rule evaluators across 9 modules
├── application/                     # Application Use Cases
│   └── detection_service.py         # DetectionService orchestrator
├── ports/                           # Input and Output boundary interfaces
│   ├── inbound.py                   # ScanProjectUseCase
│   └── outbound.py                  # ReportFormatterPort, ResultRepositoryPort
└── adapters/                        # Infrastructure Adapters
    ├── inbound/cli/main.py          # Typer & Rich CLI
    └── outbound/
        ├── parsers/
        │   └── native_ts_parser_adapter.py   # Zero-dependency regex/AST parser
        └── persistence/
            └── html_report_formatter.py      # Architecture HUD generator
```

---

## 🧪 Test Suite

```bash
uv run pytest tests/ -v
```

```
tests/test_detection_service.py::test_scan_examples            PASSED [  7%]
tests/test_detection_service.py::test_scan_summary_by_category   PASSED [ 14%]
tests/test_detection_service.py::test_scan_produces_html       PASSED [ 21%]
tests/test_parser.py::test_parse_examples                      PASSED [ 28%]
tests/test_parser.py::test_parse_detects_classes               PASSED [ 35%]
tests/test_parser.py::test_parse_detects_type_aliases          PASSED [ 42%]
tests/test_resilience_rules.py::test_unsafe_any_detected       PASSED [ 50%]
tests/test_resilience_rules.py::test_non_null_assertion_detected PASSED [ 57%]
tests/test_resilience_rules.py::test_empty_catch_detected      PASSED [ 64%]
tests/test_resilience_rules.py::test_mutable_global_detected   PASSED [ 71%]
tests/test_type_programming_rules.py::test_discriminated_union_detected PASSED [ 78%]
tests/test_type_programming_rules.py::test_conditional_type_detected    PASSED [ 85%]
tests/test_type_programming_rules.py::test_mapped_type_detected         PASSED [ 92%]
tests/test_type_programming_rules.py::test_branded_type_detected        PASSED [100%]

============================== 14 passed in 0.07s ==============================
```

---

---

## 🌐 The DPX Multi-Language Static Analysis Family (33 Languages)

| # | Language | Repository | Ecosystem & Focus |
|:---:|---|---|---|
| 1 | **Ada** | [`bivex/DPX-Ada`](https://github.com/bivex/DPX-Ada) | Ada 2012/2022, SPARK Contracts, Ravenscar Tasking, DO-178C Safety |
| 2 | **Clojure** | [`bivex/DPX`](https://github.com/bivex/DPX) | Lisp S-Expressions, Protocols, Multimethods |
| 3 | **C** | [`bivex/DPX-C`](https://github.com/bivex/DPX-C) | Memory Safety, Struct VTables, Idiomatic C11/C23 |
| 4 | **Cairo** | [`bivex/DPX-Cairo`](https://github.com/bivex/DPX-Cairo) | Starknet Smart Contracts, ZK-Rollup Invariants |
| 5 | **C++** | [`bivex/DPX-Cpp`](https://github.com/bivex/DPX-Cpp) | RAII, CRTP, Concepts, Modern C++20/23 |
| 6 | **C#** | [`bivex/DPX-CSharp`](https://github.com/bivex/DPX-CSharp) | .NET 9, Roslyn AST, Linq, Records |
| 7 | **Dart** | [`bivex/DPX-Dart`](https://github.com/bivex/DPX-Dart) | Dart 3.x, Flutter, BLoC, Riverpod, Isolates |
| 8 | **Elixir** | [`bivex/DPX-Elixir`](https://github.com/bivex/DPX-Elixir) | BEAM OTP, GenServer, Supervisors |
| 9 | **Erlang** | [`bivex/DPX-Erlang`](https://github.com/bivex/DPX-Erlang) | Fault Tolerance, Actor Model, OTP Behaviors |
| 10 | **Gleam** | [`bivex/DPX-Gleam`](https://github.com/bivex/DPX-Gleam) | Type-Safe BEAM, Actor Concurrency |
| 11 | **Go** | [`bivex/DPX-Go`](https://github.com/bivex/DPX-Go) | Goroutines, Channels, Composition, Interfaces |
| 12 | **Haskell** | [`bivex/DPX-Haskell`](https://github.com/bivex/DPX-Haskell) | Pure Functional, Monads, Typeclasses, Arrows |
| 13 | **Huff** | [`bivex/DPX-Huff`](https://github.com/bivex/DPX-Huff) | Low-Level EVM Bytecode & Opcodes |
| 14 | **Idris 2** | [`bivex/DPX-Idris2`](https://github.com/bivex/DPX-Idris2) | Dependent Types, QTT Linear Protocols, Totality, Proofs |
| 15 | **Java** | [`bivex/DPX-Java`](https://github.com/bivex/DPX-Java) | Spring Boot, Enterprise Java, JVM Invariants |
| 16 | **Julia** | [`bivex/DPX-Julia`](https://github.com/bivex/DPX-Julia) | Multiple Dispatch, Scientific Computing |
| 17 | **Kotlin** | [`bivex/DPX-Kotlin`](https://github.com/bivex/DPX-Kotlin) | Coroutines, Multiplatform, Functional DSLs |
| 18 | **Lua** | [`bivex/DPX-Lua`](https://github.com/bivex/DPX-Lua) | Metatables, Coroutines, LuaJIT, Neovim |
| 19 | **Mojo** | [`bivex/DPX-Mojo`](https://github.com/bivex/DPX-Mojo) | SIMD Hardware, Memory Lifetimes, AI Systems |
| 20 | **Move** | [`bivex/DPX-Move`](https://github.com/bivex/DPX-Move) | Aptos & Sui Resource Safety, Linear Types |
| 21 | **OCaml** | [`bivex/DPX-OCaml`](https://github.com/bivex/DPX-OCaml) | Algebraic Data Types, Functors, Polymorphism |
| 22 | **PHP** | [`bivex/DPX-Php`](https://github.com/bivex/DPX-Php) | Modern PHP 8.4, Attributes, Traits, Laravel |
| 23 | **Prolog** | [`bivex/DPX-Prolog`](https://github.com/bivex/DPX-Prolog) | ISO Prolog, SWI-Prolog, DCG, CLP(FD/R/Q), CHR, Meta-Interpreters |
| 24 | **Puppet** | [`bivex/DPX-Puppet`](https://github.com/bivex/DPX-Puppet) | Puppet DSL, Roles/Profiles, IaC Security, Hiera |
| 25 | **Python** | [`bivex/DPX-Py`](https://github.com/bivex/DPX-Py) | Metaprogramming, Protocols, Hexagonal DDD |
| 26 | **Ruby** | [`bivex/DPX-Ruby`](https://github.com/bivex/DPX-Ruby) | Ruby 3.x, Rails, Metaprogramming, Dry-RB, Security |
| 27 | **Rust** | [`bivex/DPX-Rust`](https://github.com/bivex/DPX-Rust) | Zero-Cost Abstractions, Borrow Checker, Traits |
| 28 | **Solidity** | [`bivex/DPX-Solidity`](https://github.com/bivex/DPX-Solidity) | DeFi Security, Reentrancy, EVM Yul/Assembly |
| 29 | **SQL** | [`bivex/DPX-SQL`](https://github.com/bivex/DPX-SQL) | PostgreSQL, MySQL, SQLite, T-SQL, PL/SQL |
| 30 | **Swift** | [`bivex/DPX-Swift`](https://github.com/bivex/DPX-Swift) | Protocol-Oriented Programming, Actors |
| 31 | **TypeScript** | [`bivex/DPX-TypeScript`](https://github.com/bivex/DPX-TypeScript) | Generics, Conditional Types, Clean Architecture |
| 32 | **Yul** | [`bivex/DPX-Yul`](https://github.com/bivex/DPX-Yul) | EVM Intermediate Representation Optimization |
| 33 | **Zig** | [`bivex/DPX-Zig`](https://github.com/bivex/DPX-Zig) | Comptime, Manual Memory Allocators, C ABI |

---

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.
