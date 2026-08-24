"""Type-Level Programming Rules (Discriminated Unions, Conditionals, Mapped Types, Branded Types, Type Guards)."""

from __future__ import annotations

import re
from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class DiscriminatedUnionRule(BasePatternRule):
    @property
    def pattern_type(self) -> PatternType:
        return PatternType.DISCRIMINATED_UNION

    def detect(self, model: CodeModel) -> list[Detection]:
        detections = []
        for m in model.all_modules():
            for t_name, t in m.types.items():
                if t.is_discriminated:
                    evidences = [
                        Evidence(
                            description=f"Type alias '{t_name}' defines a Discriminated / Tagged Union enabling compile-time exhaustive checks",
                            weight=0.85,
                            rule_code="DISCRIMINATED_UNION_TAG",
                            location=t.location,
                        )
                    ]
                    detections.append(self._create_detection(
                        target_name=f"{m.name}.{t_name}",
                        target_kind="discriminated_union",
                        evidences=evidences,
                        location=t.location,
                    ))
        return detections


class ConditionalTypesRule(BasePatternRule):
    @property
    def pattern_type(self) -> PatternType:
        return PatternType.CONDITIONAL_TYPES

    def detect(self, model: CodeModel) -> list[Detection]:
        detections = []
        for m in model.all_modules():
            for t_name, t in m.types.items():
                if t.is_conditional:
                    evidences = [
                        Evidence(
                            description=f"Type alias '{t_name}' uses Conditional Types (`extends ... ? :`) for type-level computation",
                            weight=0.85,
                            rule_code="CONDITIONAL_TYPE_INFER",
                            location=t.location,
                        )
                    ]
                    detections.append(self._create_detection(
                        target_name=f"{m.name}.{t_name}",
                        target_kind="conditional_type",
                        evidences=evidences,
                        location=t.location,
                    ))
        return detections


class MappedTypesRule(BasePatternRule):
    @property
    def pattern_type(self) -> PatternType:
        return PatternType.MAPPED_TYPES

    def detect(self, model: CodeModel) -> list[Detection]:
        detections = []
        for m in model.all_modules():
            for t_name, t in m.types.items():
                if t.is_mapped:
                    evidences = [
                        Evidence(
                            description=f"Type alias '{t_name}' implements Mapped / Template Literal Types (`[K in keyof T]`) for homogeneous transformation",
                            weight=0.85,
                            rule_code="MAPPED_TYPE_HOMOGENEOUS",
                            location=t.location,
                        )
                    ]
                    detections.append(self._create_detection(
                        target_name=f"{m.name}.{t_name}",
                        target_kind="mapped_type",
                        evidences=evidences,
                        location=t.location,
                    ))
        return detections


class BrandedTypesRule(BasePatternRule):
    @property
    def pattern_type(self) -> PatternType:
        return PatternType.BRANDED_TYPES

    def detect(self, model: CodeModel) -> list[Detection]:
        detections = []
        for m in model.all_modules():
            for t_name, t in m.types.items():
                if t.is_branded:
                    evidences = [
                        Evidence(
                            description=f"Type '{t_name}' enforces Nominal / Branded typing (`__brand`) at zero runtime overhead",
                            weight=0.85,
                            rule_code="BRANDED_NOMINAL_TYPE",
                            location=t.location,
                        )
                    ]
                    detections.append(self._create_detection(
                        target_name=f"{m.name}.{t_name}",
                        target_kind="branded_type",
                        evidences=evidences,
                        location=t.location,
                    ))
        return detections


class TypeGuardPredicateRule(BasePatternRule):
    @property
    def pattern_type(self) -> PatternType:
        return PatternType.TYPE_GUARD_PREDICATE

    def detect(self, model: CodeModel) -> list[Detection]:
        detections = []
        for m in model.all_modules():
            for fn_name, fn in m.functions.items():
                if fn.is_type_guard:
                    evidences = [
                        Evidence(
                            description=f"Function '{fn_name}' implements a User-Defined Type Guard Predicate (`{fn.return_type}`) for safe type narrowing",
                            weight=0.85,
                            rule_code="USER_DEFINED_TYPE_GUARD",
                            location=fn.location,
                        )
                    ]
                    detections.append(self._create_detection(
                        target_name=f"{m.name}.{fn_name}",
                        target_kind="type_guard_function",
                        evidences=evidences,
                        location=fn.location,
                    ))
        return detections
