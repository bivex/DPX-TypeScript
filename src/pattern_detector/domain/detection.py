"""Domain entities for architectural detections and reports."""

from __future__ import annotations

from pydantic import BaseModel, Field
from pattern_detector.domain.value_objects import (
    Confidence,
    ConfidenceLevel,
    Evidence,
    Location,
    PatternCategory,
    PatternType,
)


class Detection(BaseModel):
    """Represents a single detected architectural pattern or code smell."""

    pattern_type: PatternType
    pattern_category: PatternCategory
    target_name: str
    target_kind: str
    summary: str
    confidence: Confidence
    primary_location: Location | None = None
    related_locations: list[Location] = Field(default_factory=list)
    evidences: list[Evidence] = Field(default_factory=list)

    @property
    def level(self) -> ConfidenceLevel:
        return self.confidence.level


class DetectionReport(BaseModel):
    """Aggregated static analysis scan report across all project modules."""

    project_path: str
    detections: list[Detection] = Field(default_factory=list)
    scanned_files_count: int = 0
    elapsed_seconds: float = 0.0

    @property
    def total_detections_count(self) -> int:
        return len(self.detections)

    @property
    def summary_by_category(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for d in self.detections:
            cat = d.pattern_category.value
            counts[cat] = counts.get(cat, 0) + 1
        return counts

    @property
    def summary_by_type(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for d in self.detections:
            t = d.pattern_type.value
            counts[t] = counts.get(t, 0) + 1
        return counts
