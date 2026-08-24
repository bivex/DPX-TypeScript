"""Creational Pattern Rules (Builder, Factory Method, Singleton, Prototype)."""

from __future__ import annotations

import re
from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class BuilderPatternRule(BasePatternRule):
    @property
    def pattern_type(self) -> PatternType:
        return PatternType.BUILDER_PATTERN

    def detect(self, model: CodeModel) -> list[Detection]:
        detections = []
        for m in model.all_modules():
            for c_name, c in m.classes.items():
                if "Builder" in c_name or "build" in c.methods or "return this" in m.raw_source:
                    if "build(" in m.raw_source and "return this" in m.raw_source:
                        evidences = [
                            Evidence(
                                description=f"Class '{c_name}' implements Fluent Builder Pattern with method chaining and `.build()` terminator",
                                weight=0.85,
                                rule_code="FLUENT_BUILDER_CHAIN",
                                location=c.location,
                            )
                        ]
                        detections.append(self._create_detection(
                            target_name=f"{m.name}.{c_name}",
                            target_kind="builder_class",
                            evidences=evidences,
                            location=c.location,
                        ))
        return detections


class FactoryMethodRule(BasePatternRule):
    @property
    def pattern_type(self) -> PatternType:
        return PatternType.FACTORY_METHOD

    def detect(self, model: CodeModel) -> list[Detection]:
        detections = []
        for m in model.all_modules():
            for c_name, c in m.classes.items():
                if "Factory" in c_name or "create" in c.methods or "static create" in m.raw_source:
                    if "static create" in m.raw_source or "Factory" in c_name:
                        evidences = [
                            Evidence(
                                description=f"Class '{c_name}' implements Factory Method pattern encapsulating object instantiation",
                                weight=0.80,
                                rule_code="FACTORY_METHOD_CREATOR",
                                location=c.location,
                            )
                        ]
                        detections.append(self._create_detection(
                            target_name=f"{m.name}.{c_name}",
                            target_kind="factory_class",
                            evidences=evidences,
                            location=c.location,
                        ))
        return detections


class SingletonPatternRule(BasePatternRule):
    @property
    def pattern_type(self) -> PatternType:
        return PatternType.SINGLETON_PATTERN

    def detect(self, model: CodeModel) -> list[Detection]:
        detections = []
        for m in model.all_modules():
            for c_name, c in m.classes.items():
                if "getInstance" in c.methods or ("private static instance" in m.raw_source and "getInstance" in m.raw_source):
                    evidences = [
                        Evidence(
                            description=f"Class '{c_name}' implements Singleton Pattern with private instance caching and static `getInstance()`",
                            weight=0.90,
                            rule_code="SINGLETON_STATIC_INSTANCE",
                            location=c.location,
                        )
                    ]
                    detections.append(self._create_detection(
                        target_name=f"{m.name}.{c_name}",
                        target_kind="singleton_class",
                        evidences=evidences,
                        location=c.location,
                    ))
        return detections


class PrototypeCloneRule(BasePatternRule):
    @property
    def pattern_type(self) -> PatternType:
        return PatternType.PROTOTYPE_CLONE

    def detect(self, model: CodeModel) -> list[Detection]:
        detections = []
        for m in model.all_modules():
            if "structuredClone(" in m.raw_source or ".clone()" in m.raw_source or "Object.create(" in m.raw_source:
                evidences = [
                    Evidence(
                        description=f"Module '{m.name}' adopts Prototype / Structured Clone for decoupled object replication",
                        weight=0.80,
                        rule_code="PROTOTYPE_STRUCTURED_CLONE",
                        location=m.location,
                    )
                ]
                detections.append(self._create_detection(
                    target_name=m.name,
                    target_kind="prototype_module",
                    evidences=evidences,
                    location=m.location,
                ))
        return detections
