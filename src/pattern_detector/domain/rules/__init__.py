"""Rule catalog registration for TypeScript Pattern Detector — 40 rules (30 original + 10 GoF)."""

from __future__ import annotations

from pattern_detector.domain.rules.async_concurrency_rules import (
    AbortControllerCancellationRule,
    AsyncRaceConditionRule,
    StructuredPromiseAllRule,
    UnhandledPromiseRejectionRule,
)
from pattern_detector.domain.rules.base import BasePatternRule, PatternRule
from pattern_detector.domain.rules.behavioral_rules import (
    AsyncIteratorGeneratorRule,
    ChainOfResponsibilityRule,
    CommandPatternRule,
    ObserverEventEmitterRule,
    StrategyPatternRule,
)
from pattern_detector.domain.rules.creational_rules import (
    BuilderPatternRule,
    FactoryMethodRule,
    PrototypeCloneRule,
    SingletonPatternRule,
)
from pattern_detector.domain.rules.enterprise_rules import (
    DependencyInjectionRule,
    RailwayResultMonadRule,
    RepositoryPatternRule,
    SmartConstructorRule,
)
from pattern_detector.domain.rules.gof_missing_rules import (
    AbstractFactoryRule,
    BridgePatternRule,
    CompositePatternRule,
    FlyweightPatternRule,
    InterpreterPatternRule,
    MediatorPatternRule,
    MementoPatternRule,
    StatePatternRule,
    TemplateMethodRule,
    VisitorPatternRule,
)
from pattern_detector.domain.rules.quality_rules import (
    CircularModuleImportRule,
    CyclomaticComplexityKissRule,
    DuplicateCodeDryRule,
    GodModuleSrpRule,
)
from pattern_detector.domain.rules.resilience_rules import (
    MutableGlobalStateRule,
    TryCatchBlanketSwallowRule,
    UnsafeAnyAssertionRule,
    UnsafeNonNullAssertionRule,
)
from pattern_detector.domain.rules.structural_rules import (
    AdapterPatternRule,
    DecoratorPatternRule,
    FacadePatternRule,
    ProxyHandlerRule,
)
from pattern_detector.domain.rules.type_programming_rules import (
    BrandedTypesRule,
    ConditionalTypesRule,
    DiscriminatedUnionRule,
    MappedTypesRule,
    TypeGuardPredicateRule,
)

DEFAULT_RULES: list[PatternRule] = [
    # 1. Type-Level Programming & Generics (5)
    DiscriminatedUnionRule(),
    ConditionalTypesRule(),
    MappedTypesRule(),
    BrandedTypesRule(),
    TypeGuardPredicateRule(),

    # 2. Creational & Factory Patterns (5 — all GoF)
    BuilderPatternRule(),
    AbstractFactoryRule(),
    FactoryMethodRule(),
    SingletonPatternRule(),
    PrototypeCloneRule(),

    # 3. Structural Patterns (7 — all GoF)
    AdapterPatternRule(),
    BridgePatternRule(),
    CompositePatternRule(),
    DecoratorPatternRule(),
    FacadePatternRule(),
    FlyweightPatternRule(),
    ProxyHandlerRule(),

    # 4. Behavioral & Reactive Patterns (11 — all GoF + Async Iterator)
    ObserverEventEmitterRule(),
    StrategyPatternRule(),
    ChainOfResponsibilityRule(),
    CommandPatternRule(),
    AsyncIteratorGeneratorRule(),
    TemplateMethodRule(),
    StatePatternRule(),
    VisitorPatternRule(),
    MediatorPatternRule(),
    MementoPatternRule(),
    InterpreterPatternRule(),

    # 5. Architectural & Enterprise Patterns (4)
    DependencyInjectionRule(),
    RepositoryPatternRule(),
    RailwayResultMonadRule(),
    SmartConstructorRule(),

    # 6. Concurrency, Async Safety & Streams (4)
    StructuredPromiseAllRule(),
    UnhandledPromiseRejectionRule(),
    AsyncRaceConditionRule(),
    AbortControllerCancellationRule(),

    # 7. Resilience & Type Safety Hazards (4)
    UnsafeAnyAssertionRule(),
    UnsafeNonNullAssertionRule(),
    TryCatchBlanketSwallowRule(),
    MutableGlobalStateRule(),

    # 8. Principles, Complexity & Quality (4)
    GodModuleSrpRule(),
    CyclomaticComplexityKissRule(),
    DuplicateCodeDryRule(),
    CircularModuleImportRule(),
]

__all__ = [
    "BasePatternRule",
    "PatternRule",
    "DEFAULT_RULES",
    # Type programming
    "DiscriminatedUnionRule", "ConditionalTypesRule", "MappedTypesRule",
    "BrandedTypesRule", "TypeGuardPredicateRule",
    # Creational (all GoF)
    "BuilderPatternRule", "AbstractFactoryRule", "FactoryMethodRule",
    "SingletonPatternRule", "PrototypeCloneRule",
    # Structural (all GoF)
    "AdapterPatternRule", "BridgePatternRule", "CompositePatternRule",
    "DecoratorPatternRule", "FacadePatternRule", "FlyweightPatternRule", "ProxyHandlerRule",
    # Behavioral (all GoF + Async)
    "ObserverEventEmitterRule", "StrategyPatternRule", "ChainOfResponsibilityRule",
    "CommandPatternRule", "AsyncIteratorGeneratorRule", "TemplateMethodRule",
    "StatePatternRule", "VisitorPatternRule", "MediatorPatternRule",
    "MementoPatternRule", "InterpreterPatternRule",
    # Enterprise
    "DependencyInjectionRule", "RepositoryPatternRule", "RailwayResultMonadRule", "SmartConstructorRule",
    # Async
    "StructuredPromiseAllRule", "UnhandledPromiseRejectionRule",
    "AsyncRaceConditionRule", "AbortControllerCancellationRule",
    # Resilience
    "UnsafeAnyAssertionRule", "UnsafeNonNullAssertionRule",
    "TryCatchBlanketSwallowRule", "MutableGlobalStateRule",
    # Quality
    "GodModuleSrpRule", "CyclomaticComplexityKissRule",
    "DuplicateCodeDryRule", "CircularModuleImportRule",
]
