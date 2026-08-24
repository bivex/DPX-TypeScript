"""10 Missing GoF Pattern Rules — completes all 23 Gang of Four patterns for TypeScript."""

from __future__ import annotations

from pattern_detector.domain.code_model import CodeModel
from pattern_detector.domain.detection import Detection
from pattern_detector.domain.rules.base import BasePatternRule
from pattern_detector.domain.value_objects import Evidence, PatternType


# ── Creational ────────────────────────────────────────────────────────────────

class AbstractFactoryRule(BasePatternRule):
    """Detects Abstract Factory: interface with multiple `create*()` factory methods."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.ABSTRACT_FACTORY

    def detect(self, model: CodeModel) -> list[Detection]:
        detections = []
        for m in model.all_modules():
            for iface_name, iface in m.interfaces.items():
                create_methods = [mth for mth in iface.methods if mth.startswith("create")]
                if len(create_methods) >= 2:
                    evidences = [
                        Evidence(
                            description=f"Interface '{iface_name}' defines {len(create_methods)} `create*()` factory methods — Abstract Factory contract for product families",
                            weight=0.85,
                            rule_code="ABSTRACT_FACTORY_INTERFACE",
                            location=iface.location,
                        )
                    ]
                    detections.append(self._create_detection(
                        target_name=f"{m.name}.{iface_name}",
                        target_kind="abstract_factory_interface",
                        evidences=evidences,
                        location=iface.location,
                    ))
            # Also detect via class naming
            for cls_name, cls in m.classes.items():
                if "Factory" in cls_name and cls.implements_list:
                    evidences = [
                        Evidence(
                            description=f"Class '{cls_name}' implements a factory interface — concrete Abstract Factory product family",
                            weight=0.80,
                            rule_code="ABSTRACT_FACTORY_CONCRETE",
                            location=cls.location,
                        )
                    ]
                    detections.append(self._create_detection(
                        target_name=f"{m.name}.{cls_name}",
                        target_kind="abstract_factory_class",
                        evidences=evidences,
                        location=cls.location,
                    ))
        return detections


# ── Structural ────────────────────────────────────────────────────────────────

class BridgePatternRule(BasePatternRule):
    """Detects Bridge: abstraction class holding an Implementor/Device interface via constructor injection."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.BRIDGE_PATTERN

    def detect(self, model: CodeModel) -> list[Detection]:
        detections = []
        bridge_keywords = {"Device", "Renderer", "Implementor", "Implementation", "Backend", "Driver", "Engine"}
        for m in model.all_modules():
            for cls_name, cls in m.classes.items():
                if cls.is_abstract and cls.constructor_params:
                    for param in cls.constructor_params:
                        if any(kw in param for kw in bridge_keywords):
                            evidences = [
                                Evidence(
                                    description=f"Abstract class '{cls_name}' composes an Implementor (`{param}`) via constructor — Bridge Pattern decoupling abstraction from implementation",
                                    weight=0.80,
                                    rule_code="BRIDGE_ABSTRACTION_IMPLEMENTOR",
                                    location=cls.location,
                                )
                            ]
                            detections.append(self._create_detection(
                                target_name=f"{m.name}.{cls_name}",
                                target_kind="bridge_abstraction_class",
                                evidences=evidences,
                                location=cls.location,
                            ))
                            break
                # Also detect by raw source pattern
                if "Bridge" in cls_name or (cls.extends_name and "Bridge" in (cls.extends_name or "")):
                    evidences = [
                        Evidence(
                            description=f"Class '{cls_name}' uses Bridge naming convention for abstraction-implementation separation",
                            weight=0.75,
                            rule_code="BRIDGE_NAMING_CONVENTION",
                            location=cls.location,
                        )
                    ]
                    detections.append(self._create_detection(
                        target_name=f"{m.name}.{cls_name}",
                        target_kind="bridge_class",
                        evidences=evidences,
                        location=cls.location,
                    ))
        return detections


class CompositePatternRule(BasePatternRule):
    """Detects Composite: recursive tree structure where nodes and leaves share a common interface."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.COMPOSITE_PATTERN

    def detect(self, model: CodeModel) -> list[Detection]:
        detections = []
        composite_keywords = {"children", "add(", "remove(", "getChildren", "traverse", "walk"}
        for m in model.all_modules():
            for cls_name, cls in m.classes.items():
                raw = m.raw_source
                # Composite typically has a `children` array of the same type and add/remove methods
                has_children = "children" in raw and (f": {cls_name}[]" in raw or f"Array<{cls_name}>" in raw)
                has_add_remove = ("add(" in raw or "addChild(" in raw) and ("remove(" in raw or "removeChild(" in raw)
                if has_children or has_add_remove:
                    evidences = [
                        Evidence(
                            description=f"Class '{cls_name}' maintains a recursive `children` collection of the same type — Composite tree structure",
                            weight=0.85,
                            rule_code="COMPOSITE_RECURSIVE_TREE",
                            location=cls.location,
                        )
                    ]
                    detections.append(self._create_detection(
                        target_name=f"{m.name}.{cls_name}",
                        target_kind="composite_class",
                        evidences=evidences,
                        location=cls.location,
                    ))
        return detections


class FlyweightPatternRule(BasePatternRule):
    """Detects Flyweight: Map/cache-based object pool sharing intrinsic state across many instances."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.FLYWEIGHT_PATTERN

    def detect(self, model: CodeModel) -> list[Detection]:
        detections = []
        for m in model.all_modules():
            raw = m.raw_source
            # Flyweight: class with private Map/cache and a get/acquire method
            has_cache = ("private cache" in raw or "private pool" in raw or "private _cache" in raw or
                        "= new Map<" in raw and "private" in raw)
            has_get_or_acquire = ("get(" in raw or "acquire(" in raw or "getInstance(" in raw or "getOrCreate(" in raw)
            if has_cache and has_get_or_acquire:
                for cls_name, cls in m.classes.items():
                    if "Factory" in cls_name or "Pool" in cls_name or "Cache" in cls_name or "Registry" in cls_name:
                        evidences = [
                            Evidence(
                                description=f"Class '{cls_name}' maintains a private `Map` cache returning shared instances — Flyweight Object Pool pattern",
                                weight=0.80,
                                rule_code="FLYWEIGHT_OBJECT_POOL_CACHE",
                                location=cls.location,
                            )
                        ]
                        detections.append(self._create_detection(
                            target_name=f"{m.name}.{cls_name}",
                            target_kind="flyweight_pool_class",
                            evidences=evidences,
                            location=cls.location,
                        ))
        return detections


# ── Behavioral ────────────────────────────────────────────────────────────────

class TemplateMethodRule(BasePatternRule):
    """Detects Template Method: abstract class with concrete hook method calling abstract steps."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.TEMPLATE_METHOD

    def detect(self, model: CodeModel) -> list[Detection]:
        detections = []
        for m in model.all_modules():
            raw = m.raw_source
            for cls_name, cls in m.classes.items():
                if cls.is_abstract and "abstract " in raw:
                    # Template method: abstract class has a public concrete method + multiple abstract methods
                    abstract_count = raw.count("abstract ")
                    if abstract_count >= 2:
                        evidences = [
                            Evidence(
                                description=f"Abstract class '{cls_name}' defines {abstract_count} abstract hook methods — Template Method skeleton algorithm pattern",
                                weight=0.85,
                                rule_code="TEMPLATE_METHOD_ABSTRACT_HOOKS",
                                location=cls.location,
                            )
                        ]
                        detections.append(self._create_detection(
                            target_name=f"{m.name}.{cls_name}",
                            target_kind="template_method_class",
                            evidences=evidences,
                            location=cls.location,
                        ))
        return detections


class StatePatternRule(BasePatternRule):
    """Detects State Pattern: explicit state machine transitions, state objects, or discriminated union states."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.STATE_PATTERN

    def detect(self, model: CodeModel) -> list[Detection]:
        detections = []
        for m in model.all_modules():
            raw = m.raw_source
            # State via class hierarchy
            for cls_name, cls in m.classes.items():
                if "State" in cls_name and (cls.implements_list or cls.extends_name):
                    evidences = [
                        Evidence(
                            description=f"Class '{cls_name}' represents a concrete State in a State Machine pattern",
                            weight=0.80,
                            rule_code="STATE_MACHINE_CLASS_HIERARCHY",
                            location=cls.location,
                        )
                    ]
                    detections.append(self._create_detection(
                        target_name=f"{m.name}.{cls_name}",
                        target_kind="state_class",
                        evidences=evidences,
                        location=cls.location,
                    ))
            # State via discriminated union + transition function
            for t_name, t in m.types.items():
                if t.is_discriminated and ("State" in t_name or "Phase" in t_name or "Status" in t_name or "Mode" in t_name):
                    evidences = [
                        Evidence(
                            description=f"Discriminated Union '{t_name}' models explicit state machine states for type-safe transitions",
                            weight=0.85,
                            rule_code="STATE_DISCRIMINATED_UNION_FSM",
                            location=t.location,
                        )
                    ]
                    detections.append(self._create_detection(
                        target_name=f"{m.name}.{t_name}",
                        target_kind="state_union_type",
                        evidences=evidences,
                        location=t.location,
                    ))
        return detections


class VisitorPatternRule(BasePatternRule):
    """Detects Visitor: visit/accept double-dispatch mechanism for separating algorithm from structure."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.VISITOR_PATTERN

    def detect(self, model: CodeModel) -> list[Detection]:
        detections = []
        for m in model.all_modules():
            raw = m.raw_source
            for iface_name, iface in m.interfaces.items():
                visit_methods = [mth for mth in iface.methods if mth.startswith("visit")]
                if len(visit_methods) >= 1:
                    evidences = [
                        Evidence(
                            description=f"Interface '{iface_name}' declares {len(visit_methods)} `visit*()` methods — Visitor Pattern double-dispatch protocol",
                            weight=0.90,
                            rule_code="VISITOR_INTERFACE_DISPATCH",
                            location=iface.location,
                        )
                    ]
                    detections.append(self._create_detection(
                        target_name=f"{m.name}.{iface_name}",
                        target_kind="visitor_interface",
                        evidences=evidences,
                        location=iface.location,
                    ))
            # Also detect accept(visitor) pattern
            if "accept(visitor" in raw or ".accept(" in raw:
                evidences = [
                    Evidence(
                        description=f"Module '{m.name}' implements `accept(visitor)` double-dispatch — Visitor Pattern element side",
                        weight=0.85,
                        rule_code="VISITOR_ACCEPT_DISPATCH",
                        location=m.location,
                    )
                ]
                detections.append(self._create_detection(
                    target_name=m.name,
                    target_kind="visitor_acceptor_module",
                    evidences=evidences,
                    location=m.location,
                ))
        return detections


class MediatorPatternRule(BasePatternRule):
    """Detects Mediator: centralized event bus / message broker decoupling component communication."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.MEDIATOR_PATTERN

    def detect(self, model: CodeModel) -> list[Detection]:
        detections = []
        mediator_keywords = {"EventBus", "MessageBus", "Mediator", "Broker", "Hub", "Dispatcher"}
        for m in model.all_modules():
            raw = m.raw_source
            for cls_name, cls in m.classes.items():
                if any(kw in cls_name for kw in mediator_keywords):
                    evidences = [
                        Evidence(
                            description=f"Class '{cls_name}' acts as Mediator / Event Bus centralising component-to-component communication",
                            weight=0.85,
                            rule_code="MEDIATOR_EVENT_BUS_CLASS",
                            location=cls.location,
                        )
                    ]
                    detections.append(self._create_detection(
                        target_name=f"{m.name}.{cls_name}",
                        target_kind="mediator_class",
                        evidences=evidences,
                        location=cls.location,
                    ))
            # Detect via handlers Map pattern
            if ("handlers" in raw or "subscribers" in raw or "listeners" in raw) and \
               ("new Map<" in raw) and (".emit(" in raw or ".publish(" in raw or ".notify(" in raw):
                if not any(kw in m.name for kw in mediator_keywords):  # not already caught
                    evidences = [
                        Evidence(
                            description=f"Module '{m.name}' implements Mediator pattern with typed handler registry and publish/notify dispatch",
                            weight=0.80,
                            rule_code="MEDIATOR_HANDLER_REGISTRY",
                            location=m.location,
                        )
                    ]
                    detections.append(self._create_detection(
                        target_name=m.name,
                        target_kind="mediator_module",
                        evidences=evidences,
                        location=m.location,
                    ))
        return detections


class MementoPatternRule(BasePatternRule):
    """Detects Memento: history stack / snapshot-based undo-redo mechanism."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.MEMENTO_PATTERN

    def detect(self, model: CodeModel) -> list[Detection]:
        detections = []
        for m in model.all_modules():
            raw = m.raw_source
            # Memento: history array + save/restore or push/pop methods
            has_history = "history" in raw and ("[" in raw or "stack" in raw.lower() or "Stack" in raw)
            has_undo_restore = ("restore(" in raw or "undo(" in raw or "rollback(" in raw or
                               ("history.pop()" in raw and "history.push(" in raw))
            if has_history and has_undo_restore:
                evidences = [
                    Evidence(
                        description=f"Module '{m.name}' maintains a history stack with save/restore — Memento / Snapshot / Undo pattern",
                        weight=0.85,
                        rule_code="MEMENTO_HISTORY_SNAPSHOT",
                        location=m.location,
                    )
                ]
                detections.append(self._create_detection(
                    target_name=m.name,
                    target_kind="memento_module",
                    evidences=evidences,
                    location=m.location,
                ))
            # Also detect by class naming
            for cls_name, cls in m.classes.items():
                if "Memento" in cls_name or "Snapshot" in cls_name or "History" in cls_name:
                    evidences = [
                        Evidence(
                            description=f"Class '{cls_name}' represents an immutable state snapshot for Memento / undo pattern",
                            weight=0.80,
                            rule_code="MEMENTO_SNAPSHOT_CLASS",
                            location=cls.location,
                        )
                    ]
                    detections.append(self._create_detection(
                        target_name=f"{m.name}.{cls_name}",
                        target_kind="memento_class",
                        evidences=evidences,
                        location=cls.location,
                    ))
        return detections


class InterpreterPatternRule(BasePatternRule):
    """Detects Interpreter: recursive expression/AST tree with interpret(ctx) or eval() dispatch."""

    @property
    def pattern_type(self) -> PatternType:
        return PatternType.INTERPRETER_PATTERN

    def detect(self, model: CodeModel) -> list[Detection]:
        detections = []
        for m in model.all_modules():
            raw = m.raw_source
            for iface_name, iface in m.interfaces.items():
                interp_methods = [mth for mth in iface.methods
                                  if mth in ("interpret", "evaluate", "eval", "execute", "parse")]
                if interp_methods:
                    evidences = [
                        Evidence(
                            description=f"Interface '{iface_name}' declares `{interp_methods[0]}()` — Interpreter Pattern grammar expression contract",
                            weight=0.85,
                            rule_code="INTERPRETER_EXPRESSION_INTERFACE",
                            location=iface.location,
                        )
                    ]
                    detections.append(self._create_detection(
                        target_name=f"{m.name}.{iface_name}",
                        target_kind="interpreter_expression_interface",
                        evidences=evidences,
                        location=iface.location,
                    ))
            # Detect AST node naming conventions
            for cls_name, cls in m.classes.items():
                if any(kw in cls_name for kw in ("Expression", "Expr", "Statement", "Stmt", "AST", "Node")):
                    if "interpret" in raw or "evaluate" in raw or "accept(visitor" in raw:
                        evidences = [
                            Evidence(
                                description=f"Class '{cls_name}' is an AST node with interpret/evaluate — Interpreter DSL grammar element",
                                weight=0.80,
                                rule_code="INTERPRETER_AST_NODE_CLASS",
                                location=cls.location,
                            )
                        ]
                        detections.append(self._create_detection(
                            target_name=f"{m.name}.{cls_name}",
                            target_kind="interpreter_ast_class",
                            evidences=evidences,
                            location=cls.location,
                        ))
        return detections
