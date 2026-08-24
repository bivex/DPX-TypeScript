"""Domain Code Model for TypeScript & JavaScript AST abstraction."""

from __future__ import annotations

from dataclasses import dataclass, field
from pattern_detector.domain.value_objects import Location


@dataclass
class TSInterface:
    """TypeScript Interface definition."""

    name: str
    generics: list[str] = field(default_factory=list)
    properties: list[str] = field(default_factory=list)
    methods: list[str] = field(default_factory=list)
    extends_list: list[str] = field(default_factory=list)
    location: Location | None = None


@dataclass
class TSTypeAlias:
    """TypeScript Type Alias (`type Foo<T> = ...`)."""

    name: str
    generics: list[str] = field(default_factory=list)
    raw_definition: str = ""
    is_union: bool = False
    is_discriminated: bool = False
    is_mapped: bool = False
    is_conditional: bool = False
    is_branded: bool = False
    location: Location | None = None


@dataclass
class TSClass:
    """TypeScript / ES6 Class definition."""

    name: str
    implements_list: list[str] = field(default_factory=list)
    extends_name: str | None = None
    decorators: list[str] = field(default_factory=list)
    constructor_params: list[str] = field(default_factory=list)
    methods: dict[str, TSFunction] = field(default_factory=dict)
    properties: list[str] = field(default_factory=list)
    is_abstract: bool = False
    location: Location | None = None


@dataclass
class TSFunction:
    """TypeScript / ES Function or Arrow Function or Method."""

    name: str
    params: list[str] = field(default_factory=list)
    return_type: str = ""
    is_async: bool = False
    is_generator: bool = False
    is_type_guard: bool = False
    decorators: list[str] = field(default_factory=list)
    cyclomatic_complexity: int = 1
    raw_body: str = ""
    location: Location | None = None


@dataclass
class TSModule:
    """Represents a TypeScript / JavaScript source file (.ts, .tsx, .js, .jsx, .mts, .cts)."""

    path: str
    name: str
    imports: list[str] = field(default_factory=list)
    exports: list[str] = field(default_factory=list)
    classes: dict[str, TSClass] = field(default_factory=dict)
    interfaces: dict[str, TSInterface] = field(default_factory=dict)
    types: dict[str, TSTypeAlias] = field(default_factory=dict)
    functions: dict[str, TSFunction] = field(default_factory=dict)
    raw_source: str = ""
    line_count: int = 0
    location: Location | None = None


class CodeModel:
    """Aggregates all parsed TypeScript & JavaScript modules."""

    def __init__(self) -> None:
        self._modules: dict[str, TSModule] = {}

    def add_module(self, module: TSModule) -> None:
        self._modules[module.path] = module

    def get_module(self, path: str) -> TSModule | None:
        return self._modules.get(path)

    def all_modules(self) -> list[TSModule]:
        return list(self._modules.values())

    @property
    def total_modules(self) -> int:
        return len(self._modules)

    @property
    def total_lines(self) -> int:
        return sum(m.line_count for m in self._modules.values())
