"""Inbound ports for TypeScript Pattern Detector."""

from __future__ import annotations

from typing import Protocol
from pattern_detector.domain.detection import DetectionReport


class ScanProjectUseCase(Protocol):
    """Executes static analysis scan over target TypeScript / JavaScript codebase."""

    def scan(
        self,
        target_path: str,
        excludes: list[str] | None = None,
        verbose: bool = False,
    ) -> DetectionReport: ...
