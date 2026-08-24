/**
 * ReactiveApiGateway.ts — Demonstrates: Observer/EventEmitter, Middleware Chain,
 * Proxy/Metaprogramming, Strategy Pattern, Builder Pattern, Singleton, Async Race hazards.
 */

import { EventEmitter } from 'events';

// ── Builder Pattern ──────────────────────────────────────────────────────────
class RequestBuilder {
  private _url: string = '';
  private _method: 'GET' | 'POST' | 'PUT' | 'DELETE' = 'GET';
  private _headers: Record<string, string> = {};
  private _body: unknown;
  private _timeout: number = 5000;

  url(url: string) { this._url = url; return this; }
  method(m: 'GET' | 'POST' | 'PUT' | 'DELETE') { this._method = m; return this; }
  header(key: string, value: string) { this._headers[key] = value; return this; }
  body(data: unknown) { this._body = data; return this; }
  timeout(ms: number) { this._timeout = ms; return this; }
  build() { return { url: this._url, method: this._method, headers: this._headers, body: this._body, timeout: this._timeout }; }
}

// ── Singleton Registry ───────────────────────────────────────────────────────
class ServiceRegistry {
  private static instance: ServiceRegistry;
  private services = new Map<string, unknown>();

  private constructor() {}

  static getInstance(): ServiceRegistry {
    if (!ServiceRegistry.instance) {
      ServiceRegistry.instance = new ServiceRegistry();
    }
    return ServiceRegistry.instance;
  }

  register<T>(name: string, service: T): void { this.services.set(name, service); }
  resolve<T>(name: string): T { return this.services.get(name) as T; }
}

// ── Strategy Pattern (Retry) ─────────────────────────────────────────────────
interface RetryStrategy {
  shouldRetry(attempt: number, error: Error): boolean;
  delayMs(attempt: number): number;
}

class ExponentialBackoffStrategy implements RetryStrategy {
  constructor(private maxAttempts = 3, private baseDelayMs = 100) {}
  shouldRetry(attempt: number) { return attempt < this.maxAttempts; }
  delayMs(attempt: number) { return this.baseDelayMs * Math.pow(2, attempt); }
}

// ── Middleware Chain (Express-like) ──────────────────────────────────────────
type Ctx = { req: Request; res: Response; state: Record<string, unknown>; };
type Next = () => Promise<void>;
type Middleware = (ctx: Ctx, next: Next) => Promise<void>;

async function authMiddleware(ctx: Ctx, next: Next): Promise<void> {
  const token = ctx.req.headers.get('Authorization');
  if (!token) { ctx.state['error'] = 'Unauthorized'; return; }
  ctx.state['userId'] = token.replace('Bearer ', '');
  await next();
}

async function loggingMiddleware(ctx: Ctx, next: Next): Promise<void> {
  const start = Date.now();
  await next();
  console.log(`[${ctx.req.method}] ${new URL(ctx.req.url).pathname} ${Date.now() - start}ms`);
}

// ── ES6 Proxy / Metaprogramming ───────────────────────────────────────────────
function createReactiveStore<T extends object>(initialState: T, onChange: (key: string, value: unknown) => void): T {
  return new Proxy(initialState, {
    set(target, prop, value, receiver) {
      onChange(String(prop), value);
      return Reflect.set(target, prop, value, receiver);
    },
    get(target, prop, receiver) {
      return Reflect.get(target, prop, receiver);
    }
  });
}

// ── Observer / EventEmitter ──────────────────────────────────────────────────
class ApiGateway extends EventEmitter {
  private retryStrategy: RetryStrategy;

  constructor(strategy: RetryStrategy = new ExponentialBackoffStrategy()) {
    super();
    this.retryStrategy = strategy;
  }

  async request<T>(config: ReturnType<RequestBuilder['build']>): Promise<T> {
    let lastError: Error | null = null;
    for (let attempt = 0; attempt < 3; attempt++) {
      try {
        const ctrl = new AbortController();
        const timeoutId = setTimeout(() => ctrl.abort(), config.timeout);
        const response = await fetch(config.url, {
          method: config.method,
          headers: config.headers,
          body: config.body ? JSON.stringify(config.body) : undefined,
          signal: ctrl.signal,
        });
        clearTimeout(timeoutId);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const data = await response.json();
        this.emit('requestSuccess', { url: config.url, attempt });
        return data as T;
      } catch (error) {
        lastError = error as Error;
        this.emit('requestError', { url: config.url, attempt, error });
        if (!this.retryStrategy.shouldRetry(attempt, lastError)) break;
        await new Promise(resolve => setTimeout(resolve, this.retryStrategy.delayMs(attempt)));
      }
    }
    throw lastError;
  }
}

// ── Prototype / StructuredClone ───────────────────────────────────────────────
function deepClone<T>(obj: T): T {
  return structuredClone(obj);
}

// ── Async Iterator ────────────────────────────────────────────────────────────
async function* streamApiResults<T>(endpoint: string): AsyncGenerator<T> {
  let cursor: string | null = null;
  while (true) {
    const url = cursor ? `${endpoint}?cursor=${cursor}` : endpoint;
    const response = await fetch(url);
    if (!response.ok) break;
    const data = await response.json() as { items: T[]; nextCursor: string | null };
    for await (const item of data.items) yield item;
    if (!data.nextCursor) break;
    cursor = data.nextCursor;
  }
}

export { ApiGateway, RequestBuilder, ServiceRegistry, ExponentialBackoffStrategy, createReactiveStore, streamApiResults, deepClone };
export type { Middleware, RetryStrategy, Ctx, Next };
