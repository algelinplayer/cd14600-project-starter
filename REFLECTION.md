# Personal Finance Manager - Design Patterns Reflection

## 1. Singleton Pattern
**Where it fits:** Used in the `Balance` class to ensure there is only ever one source of truth for the user's financial balance across the entire application.
**Why it was chosen:** A personal finance app must maintain a single, consistent state for the user's total funds. If multiple balance objects were accidentally created, transactions could be applied to different instances, leading to incorrect totals.
**Trade-offs:** Singletons introduce global state, which can make unit testing difficult because state persists between tests. To mitigate this, I implemented a `reset()` method to clear the balance and observers before each test run.

## 2. Adapter Pattern
**Where it fits:** Used in the `TransactionAdapter` class to convert `ExternalFreelanceIncome` objects into standard `Transaction` objects.
**Why it was chosen:** The app is designed around a standard `Transaction` interface. However, gig workers often receive data from third-party platforms (like invoices) that don't match this interface. The Adapter pattern allows us to integrate these external objects without modifying the core `Transaction` logic or the external class itself.
**Trade-offs:** It adds an extra layer of abstraction and a new class to maintain. For very simple data structures, a conversion function might suffice, but the Adapter provides a clean, object-oriented way to map the incompatible interfaces.

## 3. Observer Pattern
**Where it fits:** Used in `PrintObserver` and `LowBalanceAlertObserver`, which register with the `Balance` subject to receive notifications whenever a transaction is applied.
**Why it was chosen:** The `Balance` class shouldn't need to know about all the side effects that should happen when a balance changes (like printing to the console, sending an email, or triggering an alert). The Observer pattern decouples the subject (`Balance`) from its dependents.
**Trade-offs:** Observers are notified synchronously in this implementation, meaning a slow observer could delay the transaction processing. Also, the order of observer notification is not guaranteed.

## 4. Strategy Pattern (Student's Choice)
**Where it fits:** Implemented in the `budget` package with `BudgetPlanner` as the context and `FiftyThirtyTwentyStrategy` / `ZeroBasedBudgetStrategy` as the concrete strategies. It evaluates total income and expenses against different budgeting rules.
**Why it was chosen:** Users have different financial goals and prefer different budgeting methodologies. The Strategy pattern allows the application to support multiple budgeting algorithms and even swap them at runtime without changing the core transaction or balance logic. It perfectly aligns with the Open/Closed Principle—we can add a new budgeting strategy (e.g., "Pay Yourself First") by simply creating a new class, without touching existing code.
**Trade-offs:** It increases the number of classes in the project. The client (in this case, `main.py`) must be aware of the different strategies available in order to select and instantiate the appropriate one.
