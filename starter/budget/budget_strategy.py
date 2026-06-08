# budget_strategy.py
"""
Strategy Pattern: Budget Planning Strategies

This module implements the Strategy Pattern to allow users to choose between
different budgeting strategies dynamically. Each strategy encapsulates a
different algorithm for categorizing and evaluating spending against a budget.

Why this pattern was chosen:
- It allows the app to support multiple budgeting approaches without modifying
  existing code (Open/Closed Principle).
- Strategies can be swapped at runtime, making the system flexible.
- It improves testability by isolating each algorithm in its own class.

Where it fits in the app:
- After transactions are applied, the user can evaluate their spending
  against a chosen budget strategy to get personalized recommendations.
"""

from abc import ABC, abstractmethod


class BudgetStrategy(ABC):
    """Abstract base class defining the interface for budget strategies."""

    @abstractmethod
    def evaluate(self, income, expenses):
        """
        Evaluate spending against the budget strategy.

        Args:
            income (float): Total income amount.
            expenses (float): Total expenses amount.

        Returns:
            dict: A dictionary with budget categories and their status.
        """
        pass

    @abstractmethod
    def name(self):
        """Return the name of this budget strategy."""
        pass


class FiftyThirtyTwentyStrategy(BudgetStrategy):
    """
    The 50/30/20 Rule:
    - 50% of income goes to Needs (essentials)
    - 30% of income goes to Wants (discretionary)
    - 20% of income goes to Savings
    """

    def name(self):
        return "50/30/20 Rule"

    def evaluate(self, income, expenses):
        """Evaluate spending against the 50/30/20 budget rule."""
        needs_budget = income * 0.50
        wants_budget = income * 0.30
        savings_budget = income * 0.20

        savings_actual = income - expenses
        within_budget = expenses <= (needs_budget + wants_budget)

        return {
            "strategy": self.name(),
            "income": income,
            "expenses": expenses,
            "needs_budget": needs_budget,
            "wants_budget": wants_budget,
            "savings_target": savings_budget,
            "actual_savings": savings_actual,
            "within_budget": within_budget,
            "recommendation": (
                "You are within your budget. Keep it up!"
                if within_budget
                else "You are overspending. Consider reducing discretionary expenses."
            ),
        }


class ZeroBasedBudgetStrategy(BudgetStrategy):
    """
    Zero-Based Budgeting:
    - Every dollar of income is assigned a purpose.
    - Income minus all expenses should equal zero.
    - Any surplus should be allocated to savings or debt repayment.
    """

    def name(self):
        return "Zero-Based Budgeting"

    def evaluate(self, income, expenses):
        """Evaluate spending against zero-based budgeting."""
        unallocated = income - expenses
        balanced = abs(unallocated) < 0.01

        return {
            "strategy": self.name(),
            "income": income,
            "expenses": expenses,
            "unallocated": unallocated,
            "balanced": balanced,
            "recommendation": (
                "Your budget is perfectly balanced!"
                if balanced
                else (
                    f"You have ${unallocated:.2f} unallocated. "
                    "Assign it to savings or debt repayment."
                    if unallocated > 0
                    else f"You are overspending by ${abs(unallocated):.2f}. "
                    "Review your expenses."
                )
            ),
        }


class BudgetPlanner:
    """
    Context class for the Strategy Pattern.
    Holds a reference to a BudgetStrategy and delegates evaluation to it.
    """

    def __init__(self, strategy: BudgetStrategy):
        self._strategy = strategy

    @property
    def strategy(self):
        """Get the current budget strategy."""
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: BudgetStrategy):
        """Set a new budget strategy at runtime."""
        self._strategy = strategy

    def evaluate(self, income, expenses):
        """Delegate budget evaluation to the current strategy."""
        return self._strategy.evaluate(income, expenses)

    def get_strategy_name(self):
        """Return the name of the current strategy."""
        return self._strategy.name()
