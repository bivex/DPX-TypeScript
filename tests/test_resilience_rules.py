"""Tests for resilience and type safety hazard rules."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel, TSModule
from pattern_detector.domain.rules.resilience_rules import (
    MutableGlobalStateRule,
    TryCatchBlanketSwallowRule,
    UnsafeAnyAssertionRule,
    UnsafeNonNullAssertionRule,
)


def make_module_raw(name: str, raw: str) -> TSModule:
    m = TSModule(path=f"/src/{name}.ts", name=name, raw_source=raw, line_count=raw.count("\n") + 1)
    return m


def test_unsafe_any_detected():
    model = CodeModel()
    model.add_module(make_module_raw("api", "const user = (payload as any).user;"))
    results = UnsafeAnyAssertionRule().detect(model)
    assert len(results) == 1


def test_non_null_assertion_detected():
    model = CodeModel()
    model.add_module(make_module_raw("ui", "const elem = document.getElementById('root')!.innerHTML;"))
    results = UnsafeNonNullAssertionRule().detect(model)
    assert len(results) == 1


def test_empty_catch_detected():
    model = CodeModel()
    model.add_module(make_module_raw("service", "try { save(); } catch (e) {}"))
    results = TryCatchBlanketSwallowRule().detect(model)
    assert len(results) == 1


def test_mutable_global_detected():
    model = CodeModel()
    model.add_module(make_module_raw("config", "export let globalSession: Session | null = null;"))
    results = MutableGlobalStateRule().detect(model)
    assert len(results) == 1
