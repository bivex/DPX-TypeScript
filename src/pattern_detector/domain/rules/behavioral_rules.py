"""Behavioral & Reactive Rules (Observer, Strategy, Middleware Chain, Command, Async Iterator)."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class ObserverEventEmitterRule(BasePatternRule):
    @property
    def pattern_type(self) -> PatternType:
        return PatternType.OBSERVER_EVENT_EMITTER

    def detect(self, model: CodeModel) -> list[Detection]:
        detections = []
        for m in model.all_modules():
            if "EventEmitter" in m.raw_source or "Observable" in m.raw_source or ".emit(" in m.raw_source or ".subscribe(" in m.raw_source:
                evidences = [
                    Evidence(
                        description=f"Module '{m.name}' coordinates reactive communication via Observer / EventEmitter / Observable pub-sub",
                        weight=0.85,
                        rule_code="OBSERVER_EVENT_EMITTER_PUBSUB",
                        location=m.location,
                    )
                ]
                detections.append(self._create_detection(
                    target_name=m.name,
                    target_kind="observer_module",
                    evidences=evidences,
                    location=m.location,
                ))
        return detections


class StrategyPatternRule(BasePatternRule):
    @property
    def pattern_type(self) -> PatternType:
        return PatternType.STRATEGY_PATTERN

    def detect(self, model: CodeModel) -> list[Detection]:
        detections = []
        for m in model.all_modules():
            for c_name, c in m.classes.items():
                if "Strategy" in c_name or (c.implements_list and any("Strategy" in i for i in c.implements_list)):
                    evidences = [
                        Evidence(
                            description=f"Class '{c_name}' implements Strategy Pattern providing interchangeable algorithmic behavior",
                            weight=0.85,
                            rule_code="PLUGGABLE_STRATEGY_ALGORITHM",
                            location=c.location,
                        )
                    ]
                    detections.append(self._create_detection(
                        target_name=f"{m.name}.{c_name}",
                        target_kind="strategy_class",
                        evidences=evidences,
                        location=c.location,
                    ))
        return detections


class ChainOfResponsibilityRule(BasePatternRule):
    @property
    def pattern_type(self) -> PatternType:
        return PatternType.CHAIN_OF_RESPONSIBILITY

    def detect(self, model: CodeModel) -> list[Detection]:
        detections = []
        for m in model.all_modules():
            if "(req, res, next)" in m.raw_source or "next()" in m.raw_source or "Middleware" in m.name or "use(" in m.raw_source:
                if "next()" in m.raw_source or "next: ()" in m.raw_source or "next: NextFunction" in m.raw_source:
                    evidences = [
                        Evidence(
                            description=f"Module '{m.name}' implements Middleware Chain of Responsibility pipeline (`next()`)",
                            weight=0.85,
                            rule_code="MIDDLEWARE_CHAIN_OF_RESPONSIBILITY",
                            location=m.location,
                        )
                    ]
                    detections.append(self._create_detection(
                        target_name=m.name,
                        target_kind="middleware_chain_module",
                        evidences=evidences,
                        location=m.location,
                    ))
        return detections


class CommandPatternRule(BasePatternRule):
    @property
    def pattern_type(self) -> PatternType:
        return PatternType.COMMAND_PATTERN

    def detect(self, model: CodeModel) -> list[Detection]:
        detections = []
        for m in model.all_modules():
            for c_name, c in m.classes.items():
                if "Command" in c_name or "execute" in c.methods or "dispatch" in c.methods:
                    if "execute" in c.methods or "Command" in c_name:
                        evidences = [
                            Evidence(
                                description=f"Class '{c_name}' encapsulates executable business logic in Command Pattern",
                                weight=0.80,
                                rule_code="COMMAND_DISPATCHER_ACTION",
                                location=c.location,
                            )
                        ]
                        detections.append(self._create_detection(
                            target_name=f"{m.name}.{c_name}",
                            target_kind="command_class",
                            evidences=evidences,
                            location=c.location,
                        ))
        return detections


class AsyncIteratorGeneratorRule(BasePatternRule):
    @property
    def pattern_type(self) -> PatternType:
        return PatternType.ASYNC_ITERATOR_GENERATOR

    def detect(self, model: CodeModel) -> list[Detection]:
        detections = []
        for m in model.all_modules():
            if "async function*" in m.raw_source or "Symbol.asyncIterator" in m.raw_source or "for await (" in m.raw_source:
                evidences = [
                    Evidence(
                        description=f"Module '{m.name}' consumes streaming async flows via Async Iterator / Generator (`Symbol.asyncIterator`)",
                        weight=0.85,
                        rule_code="ASYNC_ITERATOR_GENERATOR_STREAM",
                        location=m.location,
                    )
                ]
                detections.append(self._create_detection(
                    target_name=m.name,
                    target_kind="async_iterator_module",
                    evidences=evidences,
                    location=m.location,
                ))
        return detections
