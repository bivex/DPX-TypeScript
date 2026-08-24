"""Resilience, Type Safety Hazards & Code Smell Rules."""

from __future__ import annotations

import re
from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class UnsafeAnyAssertionRule(BasePatternRule):
    @property
    def pattern_type(self) -> PatternType:
        return PatternType.UNSAFE_ANY_ASSERTION

    def detect(self, model: CodeModel) -> list[Detection]:
        detections = []
        for m in model.all_modules():
            if " as any" in m.raw_source or "<any>" in m.raw_source:
                count = len(re.findall(r"\bas\s+any\b|<any>", m.raw_source))
                evidences = [
                    Evidence(
                        description=f"Type Safety Hazard: Module '{m.name}' contains {count} unsafe `as any` type bypass assertion(s); replace with `unknown` or type guards",
                        weight=0.80,
                        rule_code="UNSAFE_AS_ANY_ASSERTION",
                        location=m.location,
                    )
                ]
                detections.append(self._create_detection(
                    target_name=m.name,
                    target_kind="unsafe_any_module",
                    evidences=evidences,
                    location=m.location,
                ))
        return detections


class UnsafeNonNullAssertionRule(BasePatternRule):
    @property
    def pattern_type(self) -> PatternType:
        return PatternType.UNSAFE_NON_NULL_ASSERTION

    def detect(self, model: CodeModel) -> list[Detection]:
        detections = []
        for m in model.all_modules():
            # Check for non-null assertions like `foo!.bar` or `val!`
            if "!." in m.raw_source or "!)" in m.raw_source or "!;" in m.raw_source:
                evidences = [
                    Evidence(
                        description=f"Type Safety Hazard: Module '{m.name}' uses non-null assertions (`!`); replace with optional chaining (`?.`) or defensive guards",
                        weight=0.75,
                        rule_code="NON_NULL_FORCED_ASSERTION",
                        location=m.location,
                    )
                ]
                detections.append(self._create_detection(
                    target_name=m.name,
                    target_kind="non_null_assertion_module",
                    evidences=evidences,
                    location=m.location,
                ))
        return detections


class TryCatchBlanketSwallowRule(BasePatternRule):
    @property
    def pattern_type(self) -> PatternType:
        return PatternType.TRY_CATCH_BLANKET_SWALLOW

    def detect(self, model: CodeModel) -> list[Detection]:
        detections = []
        for m in model.all_modules():
            if re.search(r"catch\s*\([^)]*\)\s*\{\s*\}", m.raw_source):
                evidences = [
                    Evidence(
                        description=f"Resilience Anti-Pattern: Module '{m.name}' silently swallows exceptions in empty catch block `catch (e) {{}}`",
                        weight=0.85,
                        rule_code="BLANKET_CATCH_EXCEPTION_SWALLOW",
                        location=m.location,
                    )
                ]
                detections.append(self._create_detection(
                    target_name=m.name,
                    target_kind="empty_catch_hazard",
                    evidences=evidences,
                    location=m.location,
                ))
        return detections


class MutableGlobalStateRule(BasePatternRule):
    @property
    def pattern_type(self) -> PatternType:
        return PatternType.MUTABLE_GLOBAL_STATE

    def detect(self, model: CodeModel) -> list[Detection]:
        detections = []
        for m in model.all_modules():
            if re.search(r"export\s+let\s+[A-Za-z0-9_]+", m.raw_source):
                evidences = [
                    Evidence(
                        description=f"Architectural Risk: Module '{m.name}' exports mutable variable(s) (`export let ...`) creating cross-module side-effects",
                        weight=0.80,
                        rule_code="MUTABLE_EXPORT_GLOBAL_STATE",
                        location=m.location,
                    )
                ]
                detections.append(self._create_detection(
                    target_name=m.name,
                    target_kind="mutable_export_module",
                    evidences=evidences,
                    location=m.location,
                ))
        return detections
