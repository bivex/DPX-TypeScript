"""Principles, Complexity, DRY & SOLID Rules."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


class GodModuleSrpRule(BasePatternRule):
    @property
    def pattern_type(self) -> PatternType:
        return PatternType.GOD_MODULE_SRP

    def detect(self, model: CodeModel) -> list[Detection]:
        detections = []
        for m in model.all_modules():
            decl_count = len(m.classes) + len(m.functions) + len(m.interfaces) + len(m.types)
            if decl_count >= 25 or m.line_count >= 800:
                evidences = [
                    Evidence(
                        description=f"SRP Violation (God Module): Module '{m.name}' contains {decl_count} declarations across {m.line_count} lines of code; decompose into focused domain modules",
                        weight=0.85,
                        rule_code="SRP_GOD_MODULE_DECOMPOSITION",
                        location=m.location,
                    )
                ]
                detections.append(self._create_detection(
                    target_name=m.name,
                    target_kind="god_module",
                    evidences=evidences,
                    location=m.location,
                ))
        return detections


class CyclomaticComplexityKissRule(BasePatternRule):
    @property
    def pattern_type(self) -> PatternType:
        return PatternType.CYCLOMATIC_COMPLEXITY_KISS

    def detect(self, model: CodeModel) -> list[Detection]:
        detections = []
        for m in model.all_modules():
            for fn_name, fn in m.functions.items():
                if fn.cyclomatic_complexity >= 12:
                    evidences = [
                        Evidence(
                            description=f"KISS Violation (High Complexity): Function '{fn_name}' in '{m.name}' has cyclomatic complexity of {fn.cyclomatic_complexity}; refactor complex branching",
                            weight=0.75,
                            rule_code="KISS_HIGH_CYCLOMATIC_COMPLEXITY",
                            location=fn.location,
                        )
                    ]
                    detections.append(self._create_detection(
                        target_name=f"{m.name}.{fn_name}",
                        target_kind="complex_function",
                        evidences=evidences,
                        location=fn.location,
                    ))
        return detections


class DuplicateCodeDryRule(BasePatternRule):
    @property
    def pattern_type(self) -> PatternType:
        return PatternType.DUPLICATE_CODE_DRY

    def detect(self, model: CodeModel) -> list[Detection]:
        detections = []
        fn_names: dict[str, list[str]] = {}
        for m in model.all_modules():
            for fn_name in m.functions.keys():
                if len(fn_name) > 4 and fn_name not in ("constructor", "render", "handler", "execute", "run"):
                    fn_names.setdefault(fn_name, []).append(m.name)

        for fn_name, modules in fn_names.items():
            if len(modules) >= 3:
                evidences = [
                    Evidence(
                        description=f"DRY Smell: Function name '{fn_name}' repeated across {len(modules)} modules ({', '.join(modules[:3])}); extract shared utility",
                        weight=0.70,
                        rule_code="DRY_CODE_DUPLICATION",
                    )
                ]
                detections.append(self._create_detection(
                    target_name=fn_name,
                    target_kind="duplicated_identifier",
                    evidences=evidences,
                ))
        return detections


class CircularModuleImportRule(BasePatternRule):
    @property
    def pattern_type(self) -> PatternType:
        return PatternType.CIRCULAR_MODULE_IMPORT

    def detect(self, model: CodeModel) -> list[Detection]:
        detections = []
        for m in model.all_modules():
            for imp in m.imports:
                clean_imp = imp.split("/")[-1].replace(".js", "").replace(".ts", "")
                target_mod = model.get_module(clean_imp) or next((other for other in model.all_modules() if other.name == clean_imp), None)
                if target_mod and target_mod.name != m.name:
                    if any(m.name in o_imp for o_imp in target_mod.imports):
                        evidences = [
                            Evidence(
                                description=f"Circular Dependency Risk: Module '{m.name}' and '{target_mod.name}' mutually import each other risking uninitialized references",
                                weight=0.85,
                                rule_code="CIRCULAR_MODULE_IMPORT_CYCLE",
                                location=m.location,
                            )
                        ]
                        detections.append(self._create_detection(
                            target_name=f"{m.name} <-> {target_mod.name}",
                            target_kind="circular_import_cycle",
                            evidences=evidences,
                            location=m.location,
                        ))
        return detections
