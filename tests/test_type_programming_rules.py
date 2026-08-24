"""Tests for Type-Level Programming rules."""

from __future__ import annotations

import pytest
from pattern_detector.domain.code_model import CodeModel, TSModule, TSTypeAlias
from pattern_detector.domain.value_objects import Location
from pattern_detector.domain.rules.type_programming_rules import (
    BrandedTypesRule,
    ConditionalTypesRule,
    DiscriminatedUnionRule,
    MappedTypesRule,
)


def make_module(name: str, **types) -> TSModule:
    m = TSModule(path=f"/src/{name}.ts", name=name, raw_source="", line_count=10)
    for t_name, t in types.items():
        m.types[t_name] = t
    return m


def test_discriminated_union_detected():
    t = TSTypeAlias(name="Shape", is_union=True, is_discriminated=True, raw_definition="{ kind: 'circle' } | { kind: 'square' }")
    model = CodeModel()
    model.add_module(make_module("shapes", Shape=t))
    results = DiscriminatedUnionRule().detect(model)
    assert len(results) == 1
    assert "shapes.Shape" in results[0].target_name


def test_conditional_type_detected():
    t = TSTypeAlias(name="Unbox", is_conditional=True, raw_definition="T extends Promise<infer U> ? U : T")
    model = CodeModel()
    model.add_module(make_module("util", Unbox=t))
    results = ConditionalTypesRule().detect(model)
    assert len(results) == 1


def test_mapped_type_detected():
    t = TSTypeAlias(name="Nullable", is_mapped=True, raw_definition="{ [P in keyof T]: T[P] | null }")
    model = CodeModel()
    model.add_module(make_module("util", Nullable=t))
    results = MappedTypesRule().detect(model)
    assert len(results) == 1


def test_branded_type_detected():
    t = TSTypeAlias(name="UserId", is_branded=True, raw_definition="string & { __brand: 'UserId' }")
    model = CodeModel()
    model.add_module(make_module("domain", UserId=t))
    results = BrandedTypesRule().detect(model)
    assert len(results) == 1
