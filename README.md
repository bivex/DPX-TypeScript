# 🔷 DPX-TypeScript

**Hexagonal Architecture Design Pattern Detector & IDE Observability HUD for TypeScript / JavaScript**

> Part of the **DPX family** — the same Cyber-Architectural HUD used in [DPX-Haskell](https://github.com/bivex/DPX-Haskell).

---

## Features

- **30 TypeScript/JS Pattern Rules** across 8 categories
- **IDE-like Architecture HUD** — 3-pane layout with Inspector Drawer, Density Switcher, Hotspots Matrix
- **Native regex-based parser** — no `node_modules` / tsc required
- **Supports**: `.ts`, `.tsx`, `.js`, `.jsx`, `.mts`, `.cts`, `.mjs`, `.cjs`
- **AI Context export** — one-click token-optimized prompt for Claude / ChatGPT / Gemini

## Categories (30 Rules)

| Category | Rules |
|---|---|
| 🔷 Type-Level Programming | Discriminated Union, Conditional Types, Mapped Types, Branded Types, Type Guard |
| 🟢 Creational | Builder, Factory Method, Singleton, Prototype/Clone |
| 🟣 Structural | Adapter, Decorator (AOP), Facade, ES6 Proxy |
| 🟠 Behavioral & Reactive | Observer/EventEmitter, Strategy, Middleware Chain, Command, Async Iterator |
| 🏛️ Architectural | Dependency Injection, Repository, Railway Result, Smart Constructor |
| ⚡ Concurrency & Async | Promise.allSettled, Floating Promise, Race Condition, AbortController |
| 🔴 Resilience & Hazards | Unsafe `as any`, Non-null assertion `!`, Empty catch swallow, Mutable global export |
| ⚖️ Quality & Principles | God Module (SRP), Cyclomatic Complexity (KISS), DRY, Circular Import |

## Installation

```bash
pip install -e ".[dev]"
# or via uv
uv pip install -e ".[dev]"
```

## Usage

```bash
# Scan a TypeScript project
dpx-typescript scan ./src

# Scan and generate Architecture HUD report
dpx-ts scan ./src -H reports/report.html

# Exclude directories
dpx-ts scan ./src -e dist -e __tests__ -H reports/report.html
```

## Architecture HUD

```
┌────────────────────────────────────────────────────────────────────────────────┐
│ TS  DPX Architecture HUD    my-project    TypeScript Observability Engine      │
├────────────────────────────────────────────────────────────────────────────────┤
│ ARCHITECTURE HEALTH: ████████████░░░░░░░  84%                                  │
├──────────────────┬──────────────────────────────────┬──────────────────────────┤
│ ARCHITECTURE NAV │ FINDINGS STREAM                  │ INSPECTOR DRAWER         │
│ 📋 Findings      │ ┌──────────────────────────────┐ │ #1 discriminated_union   │
│ 🗺️ Hotspots      │ │ 🔷 TYPE SYSTEM          #1   │ │                          │
│                  │ │ discriminated_union           │ │ IMPACT: HIGH             │
│ FINDINGS FILTER  │ │ BankingDomain.Shape           │ │ CONF: 85% [VERY HIGH]    │
│ ◉ All     42     │ └──────────────────────────────┘ │                          │
│ 🔴 Action  8     │ ┌──────────────────────────────┐ │ EVIDENCE TRAIL           │
│ 🔷 Types  12     │ │ 🟢 CREATIONAL           #2   │ │ +85% DISCRIMINATED_UNION │
│ 🟣 Struct  4     │ │ builder_pattern               │ │                          │
│                  │ └──────────────────────────────┘ │ AI ARCHITECT ACTIONS     │
│ MODULE HOTSPOTS  │                                  │ [💡 Review]              │
│ ● BankingDomain  │                                  │ [🛠️ Refactor]            │
│ ● ApiGateway  8  │                                  │ [🔍 Explain]             │
└──────────────────┴──────────────────────────────────┴──────────────────────────┘
```

## Running Tests

```bash
uv run pytest tests/ -v
```
