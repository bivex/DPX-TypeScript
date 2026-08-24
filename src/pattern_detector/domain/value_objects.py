"""Value objects for TypeScript / JavaScript Pattern Detector."""

from __future__ import annotations

from enum import Enum
from pydantic import BaseModel, Field


class PatternCategory(str, Enum):
    """Categorization of TypeScript architectural patterns & code smells."""

    TYPE_PROGRAMMING = "type_programming"
    CREATIONAL = "creational"
    STRUCTURAL = "structural"
    BEHAVIORAL = "behavioral"
    ARCHITECTURAL = "architectural"
    CONCURRENCY_ASYNC = "concurrency_async"
    RESILIENCE = "resilience"
    PRINCIPLE = "principle"


class PatternType(str, Enum):
    """30 TypeScript / Modern JavaScript Design Patterns, Type Idioms & Smells."""

    # 1. Type-Level Programming & Generics (5)
    DISCRIMINATED_UNION = "discriminated_union"
    CONDITIONAL_TYPES = "conditional_types"
    MAPPED_TYPES = "mapped_types"
    BRANDED_TYPES = "branded_types"
    TYPE_GUARD_PREDICATE = "type_guard_predicate"

    # 2. Creational & Factory Patterns (4)
    BUILDER_PATTERN = "builder_pattern"
    FACTORY_METHOD = "factory_method"
    SINGLETON_PATTERN = "singleton_pattern"
    PROTOTYPE_CLONE = "prototype_clone"

    # 3. Structural Patterns (4)
    ADAPTER_PATTERN = "adapter_pattern"
    DECORATOR_PATTERN = "decorator_pattern"
    FACADE_PATTERN = "facade_pattern"
    PROXY_HANDLER = "proxy_handler"

    # 4. Behavioral & Reactive Patterns (5)
    OBSERVER_EVENT_EMITTER = "observer_event_emitter"
    STRATEGY_PATTERN = "strategy_pattern"
    CHAIN_OF_RESPONSIBILITY = "chain_of_responsibility"
    COMMAND_PATTERN = "command_pattern"
    ASYNC_ITERATOR_GENERATOR = "async_iterator_generator"

    # 5. Architectural & Enterprise Patterns (4)
    DEPENDENCY_INJECTION = "dependency_injection"
    REPOSITORY_PATTERN = "repository_pattern"
    RAILWAY_RESULT_MONAD = "railway_result_monad"
    SMART_CONSTRUCTOR = "smart_constructor"

    # 6. Concurrency, Async Safety & Streams (4)
    STRUCTURED_PROMISE_ALL = "structured_promise_all"
    UNHANDLED_PROMISE_REJECTION = "unhandled_promise_rejection"
    ASYNC_RACE_CONDITION = "async_race_condition"
    ABORT_CONTROLLER_CANCELLATION = "abort_controller_cancellation"

    # 7. Resilience & Type Safety Hazards (4)
    UNSAFE_ANY_ASSERTION = "unsafe_any_assertion"
    UNSAFE_NON_NULL_ASSERTION = "unsafe_non_null_assertion"
    TRY_CATCH_BLANKET_SWALLOW = "try_catch_blanket_swallow"
    MUTABLE_GLOBAL_STATE = "mutable_global_state"

    # 8. Principles, Complexity & Quality (4)
    GOD_MODULE_SRP = "god_module_srp"
    CYCLOMATIC_COMPLEXITY_KISS = "cyclomatic_complexity_kiss"
    DUPLICATE_CODE_DRY = "duplicate_code_dry"
    CIRCULAR_MODULE_IMPORT = "circular_module_import"


class ConfidenceLevel(str, Enum):
    """Confidence classification for static detections."""

    VERY_HIGH = "VERY_HIGH"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class Location(BaseModel):
    """Source code coordinates."""

    file_path: str
    line: int = 1
    col: int = 1

    def __str__(self) -> str:
        return f"{self.file_path}:{self.line}:{self.col}"


class Evidence(BaseModel):
    """Individual heuristic proof supporting an architectural detection."""

    description: str
    weight: float = Field(ge=0.0, le=1.0)
    rule_code: str
    location: Location | None = None


class Confidence(BaseModel):
    """Confidence score with percentage formatting."""

    value: float = Field(ge=0.0, le=1.0)

    @property
    def percentage_str(self) -> str:
        return f"{int(self.value * 100)}%"

    @property
    def level(self) -> ConfidenceLevel:
        if self.value >= 0.85:
            return ConfidenceLevel.VERY_HIGH
        if self.value >= 0.70:
            return ConfidenceLevel.HIGH
        if self.value >= 0.50:
            return ConfidenceLevel.MEDIUM
        return ConfidenceLevel.LOW
