"""Architectural & Enterprise Rules (Dependency Injection, Repository, Result Monad, Smart Constructor)."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class DependencyInjectionRule(BasePatternRule):
    @property
    def pattern_type(self) -> PatternType:
        return PatternType.DEPENDENCY_INJECTION

    def detect(self, model: CodeModel) -> list[Detection]:
        detections = []
        for m in model.all_modules():
            if "@Injectable" in m.raw_source or "@Inject" in m.raw_source or "Container" in m.raw_source or "inversify" in m.raw_source:
                evidences = [
                    Evidence(
                        description=f"Module '{m.name}' implements Dependency Injection / IoC Container inverting control",
                        weight=0.85,
                        rule_code="DEPENDENCY_INJECTION_IOC",
                        location=m.location,
                    )
                ]
                detections.append(self._create_detection(
                    target_name=m.name,
                    target_kind="di_provider_module",
                    evidences=evidences,
                    location=m.location,
                ))
        return detections


class RepositoryPatternRule(BasePatternRule):
    @property
    def pattern_type(self) -> PatternType:
        return PatternType.REPOSITORY_PATTERN

    def detect(self, model: CodeModel) -> list[Detection]:
        detections = []
        for m in model.all_modules():
            for c_name, c in m.classes.items():
                if "Repository" in c_name or (c.implements_list and any("Repository" in i for i in c.implements_list)):
                    evidences = [
                        Evidence(
                            description=f"Class '{c_name}' implements Repository Pattern abstracting data persistence from domain logic",
                            weight=0.85,
                            rule_code="REPOSITORY_DATA_ACCESS",
                            location=c.location,
                        )
                    ]
                    detections.append(self._create_detection(
                        target_name=f"{m.name}.{c_name}",
                        target_kind="repository_class",
                        evidences=evidences,
                        location=c.location,
                    ))
        return detections


class RailwayResultMonadRule(BasePatternRule):
    @property
    def pattern_type(self) -> PatternType:
        return PatternType.RAILWAY_RESULT_MONAD

    def detect(self, model: CodeModel) -> list[Detection]:
        detections = []
        for m in model.all_modules():
            if "Result<" in m.raw_source or "Either<" in m.raw_source or "ok(" in m.raw_source and "err(" in m.raw_source:
                evidences = [
                    Evidence(
                        description=f"Module '{m.name}' adopts Railway Result / Either Monad for total, type-safe error handling",
                        weight=0.85,
                        rule_code="RAILWAY_RESULT_EITHER_MONAD",
                        location=m.location,
                    )
                ]
                detections.append(self._create_detection(
                    target_name=m.name,
                    target_kind="result_monad_module",
                    evidences=evidences,
                    location=m.location,
                ))
        return detections


class SmartConstructorRule(BasePatternRule):
    @property
    def pattern_type(self) -> PatternType:
        return PatternType.SMART_CONSTRUCTOR

    def detect(self, model: CodeModel) -> list[Detection]:
        detections = []
        for m in model.all_modules():
            if "private constructor(" in m.raw_source and "static create(" in m.raw_source:
                evidences = [
                    Evidence(
                        description=f"Module '{m.name}' enforces domain invariants via Smart Constructor with private constructor encapsulation",
                        weight=0.85,
                        rule_code="SMART_CONSTRUCTOR_VALIDATION",
                        location=m.location,
                    )
                ]
                detections.append(self._create_detection(
                    target_name=m.name,
                    target_kind="smart_constructor_module",
                    evidences=evidences,
                    location=m.location,
                ))
        return detections
