"""Tests for the DetectionService application layer."""

from __future__ import annotations

from pattern_detector.application.detection_service import DetectionService


def test_scan_examples():
    service = DetectionService()
    report = service.scan("examples/ts_samples")
    assert report.total_detections_count > 0
    assert report.scanned_files_count >= 2


def test_scan_summary_by_category():
    service = DetectionService()
    report = service.scan("examples/ts_samples")
    assert isinstance(report.summary_by_category, dict)
    assert len(report.summary_by_category) > 0


def test_scan_produces_html():
    from pattern_detector.adapters.outbound.persistence.html_report_formatter import HtmlReportFormatter
    service = DetectionService()
    report = service.scan("examples/ts_samples")
    html = HtmlReportFormatter().format(report)
    assert "DPX Architecture HUD" in html
    assert "FINDINGS" in html
    assert len(html) > 5000
