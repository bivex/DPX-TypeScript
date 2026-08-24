"""Structural Pattern Rules (Adapter, Decorator, Facade, Proxy)."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class AdapterPatternRule(BasePatternRule):
    @property
    def pattern_type(self) -> PatternType:
        return PatternType.ADAPTER_PATTERN

    def detect(self, model: CodeModel) -> list[Detection]:
        detections = []
        for m in model.all_modules():
            for c_name, c in m.classes.items():
                if "Adapter" in c_name or (c.implements_list and "adapter" in m.name.lower()):
                    evidences = [
                        Evidence(
                            description=f"Class '{c_name}' implements Interface Adapter pattern reconciling incompatible interfaces",
                            weight=0.85,
                            rule_code="INTERFACE_ADAPTER_WRAPPER",
                            location=c.location,
                        )
                    ]
                    detections.append(self._create_detection(
                        target_name=f"{m.name}.{c_name}",
                        target_kind="adapter_class",
                        evidences=evidences,
                        location=c.location,
                    ))
        return detections


class DecoratorPatternRule(BasePatternRule):
    @property
    def pattern_type(self) -> PatternType:
        return PatternType.DECORATOR_PATTERN

    def detect(self, model: CodeModel) -> list[Detection]:
        detections = []
        for m in model.all_modules():
            for c_name, c in m.classes.items():
                if c.decorators or "@" in m.raw_source:
                    evidences = [
                        Evidence(
                            description=f"Class '{c_name}' uses TypeScript Decorators for Aspect-Oriented metaprogramming",
                            weight=0.85,
                            rule_code="TYPESCRIPT_CLASS_DECORATOR",
                            location=c.location,
                        )
                    ]
                    detections.append(self._create_detection(
                        target_name=f"{m.name}.{c_name}",
                        target_kind="decorated_class",
                        evidences=evidences,
                        location=c.location,
                    ))
        return detections


class FacadePatternRule(BasePatternRule):
    @property
    def pattern_type(self) -> PatternType:
        return PatternType.FACADE_PATTERN

    def detect(self, model: CodeModel) -> list[Detection]:
        detections = []
        for m in model.all_modules():
            for c_name, c in m.classes.items():
                if "Facade" in c_name or ("Engine" in c_name and len(c.implements_list) == 0 and len(c.properties) >= 3):
                    evidences = [
                        Evidence(
                            description=f"Class '{c_name}' implements Subsystem Facade pattern simplifying complex multi-service operations",
                            weight=0.80,
                            rule_code="SUBSYSTEM_FACADE_API",
                            location=c.location,
                        )
                    ]
                    detections.append(self._create_detection(
                        target_name=f"{m.name}.{c_name}",
                        target_kind="facade_class",
                        evidences=evidences,
                        location=c.location,
                    ))
        return detections


class ProxyHandlerRule(BasePatternRule):
    @property
    def pattern_type(self) -> PatternType:
        return PatternType.PROXY_HANDLER

    def detect(self, model: CodeModel) -> list[Detection]:
        detections = []
        for m in model.all_modules():
            if "new Proxy(" in m.raw_source:
                evidences = [
                    Evidence(
                        description=f"Module '{m.name}' instantiates ES6 Proxy (`new Proxy(...)`) for trap interception and reactive tracking",
                        weight=0.85,
                        rule_code="ES6_PROXY_TRAP_INTERCEPTION",
                        location=m.location,
                    )
                ]
                detections.append(self._create_detection(
                    target_name=m.name,
                    target_kind="proxy_module",
                    evidences=evidences,
                    location=m.location,
                ))
        return detections
