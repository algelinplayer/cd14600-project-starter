"""This module serves as the entry point for the program."""
from balance.balance import Balance
from balance.balance_observer import LowBalanceAlertObserver, PrintObserver
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory
from transaction.transaction_adapter import TransactionAdapter
from transaction.external_income_transaction import ExternalFreelanceIncome
from budget.budget_strategy import (
    BudgetPlanner,
    FiftyThirtyTwentyStrategy,
    ZeroBasedBudgetStrategy,
)


def main():
    print("=" * 60)
    print("  Personal Finance Manager for Freelancers and Gig Workers")
    print("=" * 60)
    print()

    # --- Stage 1: Singleton Balance ---
    balance = Balance.get_instance()
    balance.reset()

    # --- Stage 3: Observer Pattern ---
    # Register observers via dependency injection (passed in, not hard-coded)
    low_balance_observer = LowBalanceAlertObserver(threshold=100)
    print_observer = PrintObserver()

    balance.register_observer(print_observer)
    balance.register_observer(low_balance_observer)

    print("Adding transactions...")
    print("-" * 60)

    # --- Stage 1: Standard Transactions ---
    transactions = [
        Transaction(100, TransactionCategory.INCOME),
        Transaction(50, TransactionCategory.EXPENSE),
        Transaction(200, TransactionCategory.INCOME),
        Transaction(75, TransactionCategory.EXPENSE),
    ]

    # --- Stage 2: Adapter Pattern ---
    # Create an external income transaction (via Adapter pattern)
    freelance_income = ExternalFreelanceIncome(1200, "INV-98765", "Mobile App Project")
    adapter = TransactionAdapter(freelance_income)
    adapted_transaction = adapter.to_transaction()

    all_transactions = transactions + [adapted_transaction]

    # Apply all transactions to balance
    for txn in all_transactions:
        balance.apply_transaction(txn)

    print("-" * 60)
    print()
    print(balance.summary())
    print()

    # --- Stage 4: Strategy Pattern (Budget Planning) ---
    print("=" * 60)
    print("  Budget Evaluation")
    print("=" * 60)
    print()

    # Calculate totals for budget evaluation
    total_income = sum(
        t.amount for t in all_transactions
        if t.category == TransactionCategory.INCOME
    )
    total_expenses = sum(
        t.amount for t in all_transactions
        if t.category == TransactionCategory.EXPENSE
    )

    # Use 50/30/20 strategy first
    planner = BudgetPlanner(FiftyThirtyTwentyStrategy())
    result = planner.evaluate(total_income, total_expenses)
    print(f"Strategy: {result['strategy']}")
    print(f"  Income: ${result['income']:.2f}")
    print(f"  Expenses: ${result['expenses']:.2f}")
    print(f"  Recommendation: {result['recommendation']}")
    print()

    # Swap to Zero-Based Budgeting at runtime (Strategy Pattern)
    planner.strategy = ZeroBasedBudgetStrategy()
    result = planner.evaluate(total_income, total_expenses)
    print(f"Strategy: {result['strategy']}")
    print(f"  Income: ${result['income']:.2f}")
    print(f"  Expenses: ${result['expenses']:.2f}")
    print(f"  Recommendation: {result['recommendation']}")
    print()


if __name__ == "__main__":
    main()
