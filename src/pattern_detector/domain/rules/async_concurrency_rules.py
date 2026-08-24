"""Concurrency, Async Safety & Streams Rules."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class StructuredPromiseAllRule(BasePatternRule):
    @property
    def pattern_type(self) -> PatternType:
        return PatternType.STRUCTURED_PROMISE_ALL

    def detect(self, model: CodeModel) -> list[Detection]:
        detections = []
        for m in model.all_modules():
            if "Promise.allSettled(" in m.raw_source or "Promise.all(" in m.raw_source:
                evidences = [
                    Evidence(
                        description=f"Module '{m.name}' coordinates concurrent asynchronous operations safely via `Promise.allSettled()` / `Promise.all()`",
                        weight=0.80,
                        rule_code="STRUCTURED_PROMISE_COORDINATION",
                        location=m.location,
                    )
                ]
                detections.append(self._create_detection(
                    target_name=m.name,
                    target_kind="structured_promise_module",
                    evidences=evidences,
                    location=m.location,
                ))
        return detections


class UnhandledPromiseRejectionRule(BasePatternRule):
    @property
    def pattern_type(self) -> PatternType:
        return PatternType.UNHANDLED_PROMISE_REJECTION

    def detect(self, model: CodeModel) -> list[Detection]:
        detections = []
        for m in model.all_modules():
            # Look for floating promise patterns without await, void, or .catch
            if "new Promise(" in m.raw_source and "catch" not in m.raw_source and "await" not in m.raw_source:
                evidences = [
                    Evidence(
                        description=f"Concurrency Hazard: Module '{m.name}' creates floating promises without `await` or `.catch()` rejection handling",
                        weight=0.75,
                        rule_code="FLOATING_PROMISE_UNHANDLED_REJECTION",
                        location=m.location,
                    )
                ]
                detections.append(self._create_detection(
                    target_name=m.name,
                    target_kind="unhandled_promise_hazard",
                    evidences=evidences,
                    location=m.location,
                ))
        return detections


class AsyncRaceConditionRule(BasePatternRule):
    @property
    def pattern_type(self) -> PatternType:
        return PatternType.ASYNC_RACE_CONDITION

    def detect(self, model: CodeModel) -> list[Detection]:
        detections = []
        for m in model.all_modules():
            if "let " in m.raw_source and "await " in m.raw_source and "++" in m.raw_source:
                evidences = [
                    Evidence(
                        description=f"Concurrency Risk: Module '{m.name}' mutates shared non-atomic state across asynchronous `await` checkpoints",
                        weight=0.75,
                        rule_code="ASYNC_MUTATION_RACE_CONDITION",
                        location=m.location,
                    )
                ]
                detections.append(self._create_detection(
                    target_name=m.name,
                    target_kind="async_race_hazard",
                    evidences=evidences,
                    location=m.location,
                ))
        return detections


class AbortControllerCancellationRule(BasePatternRule):
    @property
    def pattern_type(self) -> PatternType:
        return PatternType.ABORT_CONTROLLER_CANCELLATION

    def detect(self, model: CodeModel) -> list[Detection]:
        detections = []
        for m in model.all_modules():
            if "new AbortController(" in m.raw_source or "signal.aborted" in m.raw_source:
                evidences = [
                    Evidence(
                        description=f"Module '{m.name}' implements cooperative cancellation protocol via `AbortController` and `AbortSignal`",
                        weight=0.85,
                        rule_code="ABORT_CONTROLLER_CANCELLATION",
                        location=m.location,
                    )
                ]
                detections.append(self._create_detection(
                    target_name=m.name,
                    target_kind="abort_controller_module",
                    evidences=evidences,
                    location=m.location,
                ))
        return detections
