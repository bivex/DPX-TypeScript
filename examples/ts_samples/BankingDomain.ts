/**
 * BankingDomain.ts — Example TypeScript file demonstrating DPX-detectable patterns:
 *   Discriminated Union, Branded Types, Smart Constructor, Railway Result, Repository,
 *   Dependency Injection, Command Pattern, AbortController Cancellation.
 */

import { EventEmitter } from 'events';

// ── Branded Types (nominal typing) ──────────────────────────────────────────
type Brand<K, T> = K & { readonly __brand: T };
type UserId = Brand<string, 'UserId'>;
type AccountId = Brand<string, 'AccountId'>;
type Money = Brand<number, 'Money'>;

// ── Discriminated Union ──────────────────────────────────────────────────────
type TransactionEvent =
  | { kind: 'deposit';    accountId: AccountId; amount: Money; timestamp: Date }
  | { kind: 'withdrawal'; accountId: AccountId; amount: Money; timestamp: Date }
  | { kind: 'transfer';   from: AccountId; to: AccountId; amount: Money }
  | { kind: 'freeze';     accountId: AccountId; reason: string };

// ── Conditional Type (unwrap Promise) ───────────────────────────────────────
type Awaited<T> = T extends Promise<infer U> ? U : T;
type MaybeNull<T> = T extends null | undefined ? never : T;

// ── Mapped Types ─────────────────────────────────────────────────────────────
type ReadonlyRecord<K extends string, V> = { readonly [P in K]: V };
type Nullable<T> = { [P in keyof T]: T[P] | null };

// ── Type Guard Predicate ─────────────────────────────────────────────────────
function isDeposit(event: TransactionEvent): event is { kind: 'deposit'; accountId: AccountId; amount: Money; timestamp: Date } {
  return event.kind === 'deposit';
}

// ── Railway Result / Either Monad ─────────────────────────────────────────────
type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E };

function ok<T>(value: T): Result<T, never> { return { ok: true, value }; }
function err<E>(error: E): Result<never, E> { return { ok: false, error }; }

// ── Smart Constructor with Validation ───────────────────────────────────────
class Email {
  private constructor(private readonly value: string) {}
  static create(raw: string): Result<Email, string> {
    if (!raw.includes('@')) return err(`Invalid email: ${raw}`);
    return ok(new Email(raw.trim().toLowerCase()));
  }
  toString() { return this.value; }
}

// ── Repository Interface (DIP) ───────────────────────────────────────────────
interface AccountRepository {
  findById(id: AccountId): Promise<Account | null>;
  findByUserId(userId: UserId): Promise<Account[]>;
  save(account: Account): Promise<void>;
  delete(id: AccountId): Promise<void>;
}

// ── Domain Entity ────────────────────────────────────────────────────────────
class Account {
  private _balance: Money;
  constructor(
    readonly id: AccountId,
    readonly ownerId: UserId,
    initialBalance: Money
  ) {
    this._balance = initialBalance;
  }
  get balance(): Money { return this._balance; }
}

// ── Dependency Injection (NestJS-style service) ──────────────────────────────
function Injectable() { return (target: any) => target; }
function Inject(token: string) { return (_: any, __: string, ___: number) => {}; }

@Injectable()
class AccountService extends EventEmitter {
  constructor(
    @Inject('ACCOUNT_REPO') private readonly repo: AccountRepository
  ) {
    super();
  }

  async deposit(accountId: AccountId, amount: Money): Promise<Result<Account, string>> {
    const account = await this.repo.findById(accountId);
    if (!account) return err(`Account ${accountId} not found`);
    this.emit('transactionCreated', { kind: 'deposit', accountId, amount, timestamp: new Date() });
    return ok(account);
  }

  async transfer(from: AccountId, to: AccountId, amount: Money): Promise<Result<void, string>> {
    const results = await Promise.allSettled([
      this.repo.findById(from),
      this.repo.findById(to),
    ]);
    for (const r of results) {
      if (r.status === 'rejected') return err('Account lookup failed');
    }
    return ok(undefined);
  }
}

// ── Command Pattern ──────────────────────────────────────────────────────────
interface Command<T = void> {
  execute(): Promise<Result<T, string>>;
}

class CreateAccountCommand implements Command<Account> {
  constructor(private readonly userId: UserId, private readonly initial: Money) {}
  async execute(): Promise<Result<Account, string>> {
    const id = `acc_${Date.now()}` as AccountId;
    return ok(new Account(id, this.userId, this.initial));
  }
}

// ── AbortController Cancellation ────────────────────────────────────────────
async function fetchAccountStream(
  userId: UserId,
  onAccount: (a: Account) => void,
  signal?: AbortSignal
): Promise<void> {
  const ctrl = new AbortController();
  const merged = signal ?? ctrl.signal;
  if (merged.aborted) return;
  // Simulated cancellable fetch
  await Promise.race([
    fetch(`/api/accounts?user=${userId}`, { signal: merged }),
    new Promise<never>((_, reject) => merged.addEventListener('abort', () => reject(new DOMException('Aborted', 'AbortError')))),
  ]);
}

// ── Async Iterator / Generator ───────────────────────────────────────────────
async function* pageAccounts(userId: UserId): AsyncGenerator<Account[]> {
  let page = 0;
  while (true) {
    const response = await fetch(`/api/accounts?user=${userId}&page=${page}`);
    if (!response.ok) break;
    const data = await response.json();
    if (!data.accounts?.length) break;
    yield data.accounts;
    page++;
  }
}

export { AccountService, CreateAccountCommand, Email, Account, pageAccounts, fetchAccountStream };
export type { TransactionEvent, UserId, AccountId, Money, Result, AccountRepository };
