"""Outbound ports for TypeScript Pattern Detector."""

from __future__ import annotations

from typing import Protocol
from pattern_detector.domain.detection import DetectionReport


class ReportFormatterPort(Protocol):
    """Formats DetectionReport into output presentation format (HTML, SARIF, JSON, Markdown)."""

    def format(self, report: DetectionReport) -> str: ...


class ResultRepositoryPort(Protocol):
    """Saves formatted report to disk destination."""

    def save(self, content: str, output_path: str) -> None: ...
