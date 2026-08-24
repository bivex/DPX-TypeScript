"""Pattern metadata catalog and descriptions for TypeScript / JavaScript."""

from __future__ import annotations

from pydantic import BaseModel
from pattern_detector.domain.value_objects import PatternCategory, PatternType


class PatternCatalogEntry(BaseModel):
    """Metadata description of a TypeScript pattern rule."""

    pattern_type: PatternType
    category: PatternCategory
    name: str
    description: str
    idiomatic_example: str


PATTERN_CATALOG: dict[PatternType, PatternCatalogEntry] = {
    # 1. Type-Level Programming & Generics (5)
    PatternType.DISCRIMINATED_UNION: PatternCatalogEntry(
        pattern_type=PatternType.DISCRIMINATED_UNION,
        category=PatternCategory.TYPE_PROGRAMMING,
        name="Discriminated / Tagged Union",
        description="Type-safe sum type using a literal discriminator tag property (`kind: 'circle' | 'square'`) enabling exhaustive pattern matching.",
        idiomatic_example="type Shape = { kind: 'circle'; radius: number } | { kind: 'square'; size: number };",
    ),
    PatternType.CONDITIONAL_TYPES: PatternCatalogEntry(
        pattern_type=PatternType.CONDITIONAL_TYPES,
        category=PatternCategory.TYPE_PROGRAMMING,
        name="Conditional Types & Type Inference",
        description="Type-level ternary expressions with `infer` keyword (`T extends Array<infer U> ? U : T`) for advanced type transformation.",
        idiomatic_example="type Unbox<T> = T extends Promise<infer U> ? U : T;",
    ),
    PatternType.MAPPED_TYPES: PatternCatalogEntry(
        pattern_type=PatternType.MAPPED_TYPES,
        category=PatternCategory.TYPE_PROGRAMMING,
        name="Mapped & Template Literal Types",
        description="Transforming existing type properties homogeneously (`{ [K in keyof T]: T[K] }`) or generating string templates (`${string}Changed`).",
        idiomatic_example="type Nullable<T> = { [P in keyof T]: T[P] | null };",
    ),
    PatternType.BRANDED_TYPES: PatternCatalogEntry(
        pattern_type=PatternType.BRANDED_TYPES,
        category=PatternCategory.TYPE_PROGRAMMING,
        name="Branded / Nominal Value Objects",
        description="Zero-runtime-overhead nominal typing using unique symbol branding (`type UserId = string & { readonly __brand: unique symbol }`).",
        idiomatic_example="type Brand<K, T> = K & { readonly __brand: T };\ntype UserId = Brand<string, 'UserId'>;",
    ),
    PatternType.TYPE_GUARD_PREDICATE: PatternCatalogEntry(
        pattern_type=PatternType.TYPE_GUARD_PREDICATE,
        category=PatternCategory.TYPE_PROGRAMMING,
        name="User-Defined Type Guard Predicate",
        description="Custom predicate function returning `x is T` or `asserts x is T` to narrow types safely in control flow branches.",
        idiomatic_example="function isUser(val: unknown): val is User { return typeof val === 'object' && val !== null && 'id' in val; }",
    ),

    # 2. Creational & Factory Patterns (4)
    PatternType.BUILDER_PATTERN: PatternCatalogEntry(
        pattern_type=PatternType.BUILDER_PATTERN,
        category=PatternCategory.CREATIONAL,
        name="Fluent Builder Pattern",
        description="Method chaining fluent API (`builder.select().where().build()`) constructing complex immutable objects step-by-step.",
        idiomatic_example="class QueryBuilder { select(f: string) { return this; } build() { ... } }",
    ),
    PatternType.FACTORY_METHOD: PatternCatalogEntry(
        pattern_type=PatternType.FACTORY_METHOD,
        category=PatternCategory.CREATIONAL,
        name="Factory Method / Creator",
        description="Encapsulating object instantiation behind static creators (`static create(...)`) or specialized factory classes.",
        idiomatic_example="class LoggerFactory { static create(env: string): Logger { ... } }",
    ),
    PatternType.SINGLETON_PATTERN: PatternCatalogEntry(
        pattern_type=PatternType.SINGLETON_PATTERN,
        category=PatternCategory.CREATIONAL,
        name="Singleton Module / Instance",
        description="Ensuring a class has only one global instance via private constructor and static `getInstance()` or module singleton export.",
        idiomatic_example="class Database { private static instance: Database; static getInstance() { ... } }",
    ),
    PatternType.PROTOTYPE_CLONE: PatternCatalogEntry(
        pattern_type=PatternType.PROTOTYPE_CLONE,
        category=PatternCategory.CREATIONAL,
        name="Prototype / Structured Clone",
        description="Creating duplicate objects via `clone()`, `structuredClone()`, or prototype inheritance without coupling to concrete classes.",
        idiomatic_example="const clone = <T>(obj: T): T => structuredClone(obj);",
    ),

    # 3. Structural Patterns (4)
    PatternType.ADAPTER_PATTERN: PatternCatalogEntry(
        pattern_type=PatternType.ADAPTER_PATTERN,
        category=PatternCategory.STRUCTURAL,
        name="Interface Adapter / Wrapper",
        description="Wrapping an incompatible service interface to match target client expectations without altering existing source code.",
        idiomatic_example="class PaymentAdapter implements IPaymentGateway { constructor(private legacy: LegacyApi) {} }",
    ),
    PatternType.DECORATOR_PATTERN: PatternCatalogEntry(
        pattern_type=PatternType.DECORATOR_PATTERN,
        category=PatternCategory.STRUCTURAL,
        name="TypeScript Decorators / AOP",
        description="Decorating classes, methods, or parameters (`@Injectable()`, `@Logged()`, `@Validate()`) for cross-cutting aspect-oriented concerns.",
        idiomatic_example="@Controller('/users') class UserController { @Get('/') list() { ... } }",
    ),
    PatternType.FACADE_PATTERN: PatternCatalogEntry(
        pattern_type=PatternType.FACADE_PATTERN,
        category=PatternCategory.STRUCTURAL,
        name="Subsystem Facade API",
        description="Providing a simplified top-level interface over complex multi-step subsystems and library calls.",
        idiomatic_example="class AudioVideoEngineFacade { initialize() { this.audio.init(); this.video.init(); } }",
    ),
    PatternType.PROXY_HANDLER: PatternCatalogEntry(
        pattern_type=PatternType.PROXY_HANDLER,
        category=PatternCategory.STRUCTURAL,
        name="ES6 Proxy / Metaprogramming",
        description="Intercepting fundamental object operations (get, set, apply) via `new Proxy(target, handler)` for virtualization or reactive tracking.",
        idiomatic_example="const reactive = new Proxy(state, { set(target, prop, val) { notify(); return Reflect.set(...); } });",
    ),

    # 4. Behavioral & Reactive Patterns (5)
    PatternType.OBSERVER_EVENT_EMITTER: PatternCatalogEntry(
        pattern_type=PatternType.OBSERVER_EVENT_EMITTER,
        category=PatternCategory.BEHAVIORAL,
        name="Observer / EventEmitter / Reactive Stream",
        description="Decoupled pub/sub event dispatching using Node.js `EventEmitter`, RxJS `Observable`, or custom listeners.",
        idiomatic_example="class OrderService extends EventEmitter { placeOrder() { this.emit('orderCreated', order); } }",
    ),
    PatternType.STRATEGY_PATTERN: PatternCatalogEntry(
        pattern_type=PatternType.STRATEGY_PATTERN,
        category=PatternCategory.BEHAVIORAL,
        name="Strategy Pattern",
        description="Encapsulating interchangeable algorithms into pluggable strategy objects or first-class functions.",
        idiomatic_example="type CompressionStrategy = (buf: Buffer) => Buffer;\nconst gzipStrategy: CompressionStrategy = ...;",
    ),
    PatternType.CHAIN_OF_RESPONSIBILITY: PatternCatalogEntry(
        pattern_type=PatternType.CHAIN_OF_RESPONSIBILITY,
        category=PatternCategory.BEHAVIORAL,
        name="Middleware Chain / Pipeline",
        description="Passing requests sequentially through a chain of handlers (`(req, res, next) => next()`) in Express, Koa, or Redux middleware.",
        idiomatic_example="app.use((req, res, next) => { auth(req); next(); });",
    ),
    PatternType.COMMAND_PATTERN: PatternCatalogEntry(
        pattern_type=PatternType.COMMAND_PATTERN,
        category=PatternCategory.BEHAVIORAL,
        name="Command / Dispatcher Action",
        description="Encapsulating actions as discrete payload objects (`{ type: 'INCREMENT', payload: 1 }`) for dispatching and undo/redo.",
        idiomatic_example="interface Command { execute(): Promise<void>; }\nclass CreateUserCommand implements Command { ... }",
    ),
    PatternType.ASYNC_ITERATOR_GENERATOR: PatternCatalogEntry(
        pattern_type=PatternType.ASYNC_ITERATOR_GENERATOR,
        category=PatternCategory.BEHAVIORAL,
        name="Async Iterator / Generator Stream",
        description="Consuming asynchronous data streams lazily on demand via `for await (const chunk of stream)` and `async function*`.",
        idiomatic_example="async function* fetchPages() { while (hasNext) { yield await fetchNext(); } }",
    ),

    # 5. Architectural & Enterprise Patterns (4)
    PatternType.DEPENDENCY_INJECTION: PatternCatalogEntry(
        pattern_type=PatternType.DEPENDENCY_INJECTION,
        category=PatternCategory.ARCHITECTURAL,
        name="Dependency Injection (IoC Container)",
        description="Inverting control via constructor injection and InversifyJS / NestJS provider decorators eliminating direct instantiation.",
        idiomatic_example="@Injectable() class UserService { constructor(@Inject('DB') private db: Database) {} }",
    ),
    PatternType.REPOSITORY_PATTERN: PatternCatalogEntry(
        pattern_type=PatternType.REPOSITORY_PATTERN,
        category=PatternCategory.ARCHITECTURAL,
        name="Repository Data Access Pattern",
        description="Mediating between domain entities and database storage engines (Prisma, TypeORM, Drizzle) behind generic CRUD interfaces.",
        idiomatic_example="interface UserRepository { findById(id: UserId): Promise<User | null>; save(u: User): Promise<void>; }",
    ),
    PatternType.RAILWAY_RESULT_MONAD: PatternCatalogEntry(
        pattern_type=PatternType.RAILWAY_RESULT_MONAD,
        category=PatternCategory.ARCHITECTURAL,
        name="Railway Result / Either Monad",
        description="Handling functional error flows explicitly via `Result<T, E> = Ok<T> | Err<E>` avoiding untyped runtime exceptions.",
        idiomatic_example="type Result<T, E> = { ok: true; value: T } | { ok: false; error: E };",
    ),
    PatternType.SMART_CONSTRUCTOR: PatternCatalogEntry(
        pattern_type=PatternType.SMART_CONSTRUCTOR,
        category=PatternCategory.ARCHITECTURAL,
        name="Smart Constructor & Validation",
        description="Restricting direct object creation with private constructors and validation functions (`createEmail(...) -> Result<Email, ValidationError>`).",
        idiomatic_example="class Email { private constructor(val: string) {} static create(val: string): Result<Email, string> { ... } }",
    ),

    # 6. Concurrency, Async Safety & Streams (4)
    PatternType.STRUCTURED_PROMISE_ALL: PatternCatalogEntry(
        pattern_type=PatternType.STRUCTURED_PROMISE_ALL,
        category=PatternCategory.CONCURRENCY_ASYNC,
        name="Structured Concurrency (allSettled)",
        description="Coordinating parallel async operations safely using `Promise.allSettled()` avoiding unhandled short-circuit crashes.",
        idiomatic_example="const results = await Promise.allSettled(tasks.map(t => runTask(t)));",
    ),
    PatternType.UNHANDLED_PROMISE_REJECTION: PatternCatalogEntry(
        pattern_type=PatternType.UNHANDLED_PROMISE_REJECTION,
        category=PatternCategory.CONCURRENCY_ASYNC,
        name="Floating Promise / Missing Await",
        description="Calling asynchronous functions without `await`, `void`, or `.catch()`, risking silent unhandled rejections.",
        idiomatic_example="async function bad() { doAsyncWork(); /* missing await */ }",
    ),
    PatternType.ASYNC_RACE_CONDITION: PatternCatalogEntry(
        pattern_type=PatternType.ASYNC_RACE_CONDITION,
        category=PatternCategory.CONCURRENCY_ASYNC,
        name="Async State Mutation Race Hazard",
        description="Mutating shared state across multiple `await` checkpoints without mutex locking or atomic updates.",
        idiomatic_example="let count = 0;\nasync function increment() { const val = count; await delay(10); count = val + 1; }",
    ),
    PatternType.ABORT_CONTROLLER_CANCELLATION: PatternCatalogEntry(
        pattern_type=PatternType.ABORT_CONTROLLER_CANCELLATION,
        category=PatternCategory.CONCURRENCY_ASYNC,
        name="AbortController Cancellation Protocol",
        description="Propagating cooperative async cancellation and timeouts via `AbortController` and `signal.aborted`.",
        idiomatic_example="const ctrl = new AbortController();\nfetch(url, { signal: ctrl.signal });",
    ),

    # 7. Resilience & Type Safety Hazards (4)
    PatternType.UNSAFE_ANY_ASSERTION: PatternCatalogEntry(
        pattern_type=PatternType.UNSAFE_ANY_ASSERTION,
        category=PatternCategory.RESILIENCE,
        name="Unsafe 'as any' Type Cast",
        description="Bypassing TypeScript compiler type safety with explicit `as any` assertion casts.",
        idiomatic_example="const user = (payload as any).user;",
    ),
    PatternType.UNSAFE_NON_NULL_ASSERTION: PatternCatalogEntry(
        pattern_type=PatternType.UNSAFE_NON_NULL_ASSERTION,
        category=PatternCategory.RESILIENCE,
        name="Unsafe Non-Null Assertion (!)",
        description="Forcing null/undefined omission with `!` operator without runtime guard verification.",
        idiomatic_example="const elem = document.getElementById('root')!;",
    ),
    PatternType.TRY_CATCH_BLANKET_SWALLOW: PatternCatalogEntry(
        pattern_type=PatternType.TRY_CATCH_BLANKET_SWALLOW,
        category=PatternCategory.RESILIENCE,
        name="Empty / Blanket Catch Swallow",
        description="Catching exceptions in `try { ... } catch (e) {}` and silently swallowing them without logging or handling.",
        idiomatic_example="try { save(); } catch (e) {} /* empty swallow */",
    ),
    PatternType.MUTABLE_GLOBAL_STATE: PatternCatalogEntry(
        pattern_type=PatternType.MUTABLE_GLOBAL_STATE,
        category=PatternCategory.RESILIENCE,
        name="Mutable Global Variable Export",
        description="Exporting mutable variables (`export let config = ...`) creating unpredictable side-effects across module boundaries.",
        idiomatic_example="export let globalSession: Session | null = null;",
    ),

    # 8. Principles, Complexity & Quality (4)
    PatternType.GOD_MODULE_SRP: PatternCatalogEntry(
        pattern_type=PatternType.GOD_MODULE_SRP,
        category=PatternCategory.PRINCIPLE,
        name="Single Responsibility (God Module)",
        description="Monolithic TypeScript module defining excessive exports, classes, and lines of code (≥30 declarations or ≥800 LOC).",
        idiomatic_example="30+ class/function exports in a single file.",
    ),
    PatternType.CYCLOMATIC_COMPLEXITY_KISS: PatternCatalogEntry(
        pattern_type=PatternType.CYCLOMATIC_COMPLEXITY_KISS,
        category=PatternCategory.PRINCIPLE,
        name="KISS Cyclomatic Complexity",
        description="Function with excessive branching paths (if/else, switch case, ternary loops ≥12 branches).",
        idiomatic_example="function complexParser() { 15 switch cases and nested ifs }",
    ),
    PatternType.DUPLICATE_CODE_DRY: PatternCatalogEntry(
        pattern_type=PatternType.DUPLICATE_CODE_DRY,
        category=PatternCategory.PRINCIPLE,
        name="Don't Repeat Yourself (DRY)",
        description="Substantial duplicate function implementations across multiple files.",
        idiomatic_example="Duplicated code blocks across modules.",
    ),
    PatternType.CIRCULAR_MODULE_IMPORT: PatternCatalogEntry(
        pattern_type=PatternType.CIRCULAR_MODULE_IMPORT,
        category=PatternCategory.PRINCIPLE,
        name="Circular Module Import Cycle",
        description="Cyclic cross-module `import` dependencies causing `undefined` runtime references during initialization.",
        idiomatic_example="A imports B, and B imports A.",
    ),

    # ── Missing GoF: Creational ───────────────────────────────────────────────
    PatternType.ABSTRACT_FACTORY: PatternCatalogEntry(
        pattern_type=PatternType.ABSTRACT_FACTORY,
        category=PatternCategory.CREATIONAL,
        name="Abstract Factory",
        description="Providing an interface for creating families of related or dependent objects without specifying their concrete classes (`createButton()`, `createDialog()` per platform).",
        idiomatic_example="interface UIFactory { createButton(): Button; createDialog(): Dialog; }\nclass MacUIFactory implements UIFactory { ... }",
    ),

    # ── Missing GoF: Structural ───────────────────────────────────────────────
    PatternType.BRIDGE_PATTERN: PatternCatalogEntry(
        pattern_type=PatternType.BRIDGE_PATTERN,
        category=PatternCategory.STRUCTURAL,
        name="Bridge Pattern",
        description="Decoupling an abstraction from its implementation so both can vary independently via composition over inheritance (`Abstraction` holds reference to `Implementor`).",
        idiomatic_example="class RemoteControl { constructor(private device: Device) {} toggle() { this.device.isEnabled() ? this.device.disable() : this.device.enable(); } }",
    ),
    PatternType.COMPOSITE_PATTERN: PatternCatalogEntry(
        pattern_type=PatternType.COMPOSITE_PATTERN,
        category=PatternCategory.STRUCTURAL,
        name="Composite / Tree Structure",
        description="Composing objects into tree structures to represent part-whole hierarchies so clients treat individual objects and compositions uniformly (`Component | Leaf | Composite`).",
        idiomatic_example="interface FileSystemItem { size(): number; }\nclass Directory implements FileSystemItem { children: FileSystemItem[] = []; size() { return this.children.reduce((s, c) => s + c.size(), 0); } }",
    ),
    PatternType.FLYWEIGHT_PATTERN: PatternCatalogEntry(
        pattern_type=PatternType.FLYWEIGHT_PATTERN,
        category=PatternCategory.STRUCTURAL,
        name="Flyweight / Object Pool",
        description="Sharing fine-grained objects efficiently using an intrinsic state cache/pool to reduce memory overhead for large numbers of similar objects.",
        idiomatic_example="class GlyphFactory { private cache = new Map<string, Glyph>(); get(char: string) { if (!this.cache.has(char)) this.cache.set(char, new Glyph(char)); return this.cache.get(char)!; } }",
    ),

    # ── Missing GoF: Behavioral ───────────────────────────────────────────────
    PatternType.TEMPLATE_METHOD: PatternCatalogEntry(
        pattern_type=PatternType.TEMPLATE_METHOD,
        category=PatternCategory.BEHAVIORAL,
        name="Template Method",
        description="Defining the skeleton of an algorithm in an abstract base class, deferring specific steps to subclasses without changing the algorithm structure.",
        idiomatic_example="abstract class DataMiner { mine() { this.extractData(); this.parseData(); this.analyzeData(); } abstract extractData(): void; abstract parseData(): void; }",
    ),
    PatternType.STATE_PATTERN: PatternCatalogEntry(
        pattern_type=PatternType.STATE_PATTERN,
        category=PatternCategory.BEHAVIORAL,
        name="State Machine / State Pattern",
        description="Allowing an object to alter its behaviour when its internal state changes via explicit state objects or discriminated union state transitions.",
        idiomatic_example="type TrafficLight = 'red' | 'yellow' | 'green';\nfunction next(state: TrafficLight): TrafficLight { const transitions = { red: 'green', green: 'yellow', yellow: 'red' }; return transitions[state]; }",
    ),
    PatternType.VISITOR_PATTERN: PatternCatalogEntry(
        pattern_type=PatternType.VISITOR_PATTERN,
        category=PatternCategory.BEHAVIORAL,
        name="Visitor Pattern",
        description="Separating an algorithm from the object structure it operates on by adding a `visit` / `accept` dispatch double-dispatch mechanism.",
        idiomatic_example="interface ASTVisitor { visitBinaryExpr(node: BinaryExpr): void; visitLiteral(node: Literal): void; }\nclass Printer implements ASTVisitor { visitLiteral(node) { console.log(node.value); } }",
    ),
    PatternType.MEDIATOR_PATTERN: PatternCatalogEntry(
        pattern_type=PatternType.MEDIATOR_PATTERN,
        category=PatternCategory.BEHAVIORAL,
        name="Mediator / Event Bus",
        description="Reducing coupling between components by having them communicate exclusively through a central mediator / event bus / message broker.",
        idiomatic_example="class EventBus { private handlers = new Map<string, Function[]>(); on(event: string, fn: Function) { ... } emit(event: string, data: unknown) { ... } }",
    ),
    PatternType.MEMENTO_PATTERN: PatternCatalogEntry(
        pattern_type=PatternType.MEMENTO_PATTERN,
        category=PatternCategory.BEHAVIORAL,
        name="Memento / Snapshot / Undo",
        description="Capturing and externalising an object's internal state as an immutable snapshot to allow restoring to a previous state without violating encapsulation.",
        idiomatic_example="class Editor { private history: EditorState[] = []; save() { this.history.push({ ...this.state }); } restore() { this.state = this.history.pop()!; } }",
    ),
    PatternType.INTERPRETER_PATTERN: PatternCatalogEntry(
        pattern_type=PatternType.INTERPRETER_PATTERN,
        category=PatternCategory.BEHAVIORAL,
        name="Interpreter / DSL Parser",
        description="Defining a grammar and interpreter for a domain-specific language (DSL) using recursive expression trees (`Expression.interpret(ctx)`).",
        idiomatic_example="interface Expression { interpret(ctx: Context): number; }\nclass Add implements Expression { constructor(private l: Expression, private r: Expression) {} interpret(ctx) { return this.l.interpret(ctx) + this.r.interpret(ctx); } }",
    ),
}
