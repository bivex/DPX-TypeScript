"""Tests for the native TypeScript parser adapter."""

from __future__ import annotations

from pattern_detector.adapters.outbound.parsers.native_ts_parser_adapter import NativeTypeScriptParserAdapter


def test_parse_examples():
    parser = NativeTypeScriptParserAdapter()
    model = parser.parse_project("examples/ts_samples")
    assert model.total_modules >= 2


def test_parse_detects_classes():
    parser = NativeTypeScriptParserAdapter()
    model = parser.parse_project("examples/ts_samples")
    all_classes = {}
    for m in model.all_modules():
        all_classes.update(m.classes)
    assert len(all_classes) > 0


def test_parse_detects_type_aliases():
    parser = NativeTypeScriptParserAdapter()
    model = parser.parse_project("examples/ts_samples")
    all_types = {}
    for m in model.all_modules():
        all_types.update(m.types)
    assert len(all_types) > 0
