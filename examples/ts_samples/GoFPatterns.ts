/**
 * GoFPatterns.ts — Demonstrates all 10 previously missing GoF patterns:
 *   Abstract Factory, Bridge, Composite, Flyweight,
 *   Template Method, State Machine, Visitor, Mediator, Memento, Interpreter
 */

// ── Abstract Factory ─────────────────────────────────────────────────────────
interface Button { render(): string; }
interface Dialog { open(): void; }

interface UIFactory {
  createButton(): Button;
  createDialog(): Dialog;
}

class MacButton implements Button { render() { return '<mac-button/>'; } }
class MacDialog implements Dialog { open() { console.log('Mac Dialog'); } }
class MacUIFactory implements UIFactory {
  createButton() { return new MacButton(); }
  createDialog() { return new MacDialog(); }
}

class WindowsButton implements Button { render() { return '<win-button/>'; } }
class WindowsDialog implements Dialog { open() { console.log('Win Dialog'); } }
class WindowsUIFactory implements UIFactory {
  createButton() { return new WindowsButton(); }
  createDialog() { return new WindowsDialog(); }
}

// ── Bridge Pattern ───────────────────────────────────────────────────────────
interface Device {
  isEnabled(): boolean;
  enable(): void;
  disable(): void;
  getVolume(): number;
  setVolume(vol: number): void;
}

class TV implements Device {
  private on = false;
  private volume = 30;
  isEnabled() { return this.on; }
  enable() { this.on = true; }
  disable() { this.on = false; }
  getVolume() { return this.volume; }
  setVolume(v: number) { this.volume = v; }
}

abstract class RemoteControl {
  constructor(protected device: Device) {}
  toggle() { this.device.isEnabled() ? this.device.disable() : this.device.enable(); }
  volumeUp() { this.device.setVolume(this.device.getVolume() + 10); }
  abstract mute(): void;
}

class BasicRemote extends RemoteControl {
  mute() { this.device.setVolume(0); }
}

// ── Composite / Tree Structure ────────────────────────────────────────────────
interface FileSystemItem {
  name: string;
  size(): number;
  print(indent?: string): void;
}

class File implements FileSystemItem {
  constructor(readonly name: string, private _size: number) {}
  size() { return this._size; }
  print(indent = '') { console.log(`${indent}📄 ${this.name} (${this._size}B)`); }
}

class Directory implements FileSystemItem {
  children: FileSystemItem[] = [];
  constructor(readonly name: string) {}
  add(item: FileSystemItem) { this.children.push(item); return this; }
  remove(item: FileSystemItem) { this.children = this.children.filter(c => c !== item); }
  size() { return this.children.reduce((s, c) => s + c.size(), 0); }
  print(indent = '') {
    console.log(`${indent}📁 ${this.name}/`);
    this.children.forEach(c => c.print(indent + '  '));
  }
}

// ── Flyweight / Object Pool ──────────────────────────────────────────────────
class Glyph { constructor(readonly char: string) {} }

class GlyphFactory {
  private cache = new Map<string, Glyph>();
  get(char: string): Glyph {
    if (!this.cache.has(char)) this.cache.set(char, new Glyph(char));
    return this.cache.get(char)!;
  }
  getCacheSize() { return this.cache.size; }
}

// ── Template Method ──────────────────────────────────────────────────────────
abstract class DataMiner {
  mine(path: string): void {
    const raw = this.extractData(path);
    const parsed = this.parseData(raw);
    const result = this.analyzeData(parsed);
    this.sendReport(result);
  }
  abstract extractData(path: string): string;
  abstract parseData(raw: string): unknown[];
  protected analyzeData(data: unknown[]): string { return `Found ${data.length} records`; }
  protected sendReport(report: string): void { console.log(`Report: ${report}`); }
}

class CsvMiner extends DataMiner {
  extractData(path: string) { return `csv:${path}`; }
  parseData(raw: string) { return raw.split(','); }
}

class JsonMiner extends DataMiner {
  extractData(path: string) { return `json:${path}`; }
  parseData(raw: string) { return [JSON.parse(`{"data":"${raw}"}`)]; }
}

// ── State Machine ────────────────────────────────────────────────────────────
type TrafficLightState = 'red' | 'yellow' | 'green';

const transitions: Record<TrafficLightState, TrafficLightState> = {
  red: 'green',
  green: 'yellow',
  yellow: 'red',
};

function nextLight(state: TrafficLightState): TrafficLightState {
  return transitions[state];
}

class TrafficLight {
  private state: TrafficLightState = 'red';
  next() { this.state = nextLight(this.state); }
  current() { return this.state; }
}

// ── Visitor Pattern ──────────────────────────────────────────────────────────
interface ASTNode {
  accept(visitor: ASTVisitor): unknown;
}
interface ASTVisitor {
  visitLiteral(node: Literal): unknown;
  visitBinaryExpr(node: BinaryExpr): unknown;
  visitIdentifier(node: Identifier): unknown;
}

class Literal implements ASTNode {
  constructor(readonly value: number) {}
  accept(v: ASTVisitor) { return v.visitLiteral(this); }
}
class Identifier implements ASTNode {
  constructor(readonly name: string) {}
  accept(v: ASTVisitor) { return v.visitIdentifier(this); }
}
class BinaryExpr implements ASTNode {
  constructor(readonly left: ASTNode, readonly op: '+' | '-' | '*', readonly right: ASTNode) {}
  accept(v: ASTVisitor) { return v.visitBinaryExpr(this); }
}

class Evaluator implements ASTVisitor {
  visitLiteral(node: Literal) { return node.value; }
  visitIdentifier(_: Identifier) { return 0; }
  visitBinaryExpr(node: BinaryExpr): number {
    const l = node.left.accept(this) as number;
    const r = node.right.accept(this) as number;
    if (node.op === '+') return l + r;
    if (node.op === '-') return l - r;
    return l * r;
  }
}

// ── Mediator / Event Bus ──────────────────────────────────────────────────────
type Handler<T = unknown> = (data: T) => void;

class EventBus {
  private handlers = new Map<string, Handler[]>();

  on<T>(event: string, fn: Handler<T>): void {
    if (!this.handlers.has(event)) this.handlers.set(event, []);
    this.handlers.get(event)!.push(fn as Handler);
  }

  off(event: string, fn: Handler): void {
    const list = this.handlers.get(event) ?? [];
    this.handlers.set(event, list.filter(h => h !== fn));
  }

  emit<T>(event: string, data: T): void {
    (this.handlers.get(event) ?? []).forEach(fn => fn(data));
  }
}

// ── Memento / Snapshot / Undo ─────────────────────────────────────────────────
interface EditorState { content: string; cursor: number; }

class TextEditor {
  private state: EditorState = { content: '', cursor: 0 };
  private history: EditorState[] = [];

  type(text: string): void {
    this.save();
    this.state = { content: this.state.content + text, cursor: this.state.cursor + text.length };
  }

  save(): void {
    this.history.push({ ...this.state });
  }

  restore(): void {
    const prev = this.history.pop();
    if (prev) this.state = prev;
  }

  getContent() { return this.state.content; }
}

// ── Interpreter / DSL Parser ──────────────────────────────────────────────────
interface Expression {
  interpret(ctx: Map<string, number>): number;
}

class NumberLiteral implements Expression {
  constructor(private value: number) {}
  interpret(_ctx: Map<string, number>) { return this.value; }
}

class Variable implements Expression {
  constructor(private name: string) {}
  interpret(ctx: Map<string, number>) { return ctx.get(this.name) ?? 0; }
}

class Add implements Expression {
  constructor(private left: Expression, private right: Expression) {}
  interpret(ctx: Map<string, number>) { return this.left.interpret(ctx) + this.right.interpret(ctx); }
}

class Multiply implements Expression {
  constructor(private left: Expression, private right: Expression) {}
  interpret(ctx: Map<string, number>) { return this.left.interpret(ctx) * this.right.interpret(ctx); }
}

// Usage
const ctx = new Map([['x', 5], ['y', 3]]);
const expr = new Add(new Variable('x'), new Multiply(new NumberLiteral(2), new Variable('y'))); // x + 2*y = 11
console.log(expr.interpret(ctx)); // 11

export {
  MacUIFactory, WindowsUIFactory, BasicRemote, TV,
  Directory, File, GlyphFactory,
  CsvMiner, JsonMiner, TrafficLight,
  Evaluator, BinaryExpr, Literal, Identifier,
  EventBus, TextEditor, Add, Multiply, Variable, NumberLiteral,
};
export type { UIFactory, Device, FileSystemItem, ASTNode, ASTVisitor, Expression };
