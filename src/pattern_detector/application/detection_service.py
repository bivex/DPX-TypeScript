"""Application detection service orchestrating TypeScript static analysis."""

from __future__ import annotations

import time
from pattern_detector.adapters.outbound.parsers.native_ts_parser_adapter import NativeTypeScriptParserAdapter
from pattern_detector.domain.detection import DetectionReport
from pattern_detector.domain.rules import DEFAULT_RULES
from pattern_detector.domain.rules.base import PatternRule
from pattern_detector.ports.inbound import ScanProjectUseCase


class DetectionService(ScanProjectUseCase):
    """Core domain orchestrator executing rule evaluation over parsed TypeScript AST models."""

    def __init__(
        self,
        parser: NativeTypeScriptParserAdapter | None = None,
        rules: list[PatternRule] | None = None,
    ) -> None:
        self._parser = parser or NativeTypeScriptParserAdapter()
        self._rules = rules or list(DEFAULT_RULES)

    def scan(
        self,
        target_path: str,
        excludes: list[str] | None = None,
        verbose: bool = False,
    ) -> DetectionReport:
        start_time = time.perf_counter()

        model = self._parser.parse_project(target_path, excludes=excludes)

        detections = []
        for rule in self._rules:
            dets = rule.detect(model)
            detections.extend(dets)

        elapsed = time.perf_counter() - start_time

        return DetectionReport(
            project_path=target_path,
            detections=detections,
            scanned_files_count=model.total_modules,
            elapsed_seconds=elapsed,
        )
