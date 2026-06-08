import unittest
from budget.budget_strategy import (
    FiftyThirtyTwentyStrategy,
    ZeroBasedBudgetStrategy,
    BudgetPlanner,
)


class TestFiftyThirtyTwentyStrategy(unittest.TestCase):

    def setUp(self):
        self.strategy = FiftyThirtyTwentyStrategy()

    def test_name(self):
        self.assertEqual(self.strategy.name(), "50/30/20 Rule")

    def test_within_budget(self):
        result = self.strategy.evaluate(income=1000, expenses=700)
        self.assertTrue(result["within_budget"])
        self.assertEqual(result["needs_budget"], 500)
        self.assertEqual(result["wants_budget"], 300)
        self.assertEqual(result["savings_target"], 200)
        self.assertEqual(result["actual_savings"], 300)

    def test_over_budget(self):
        result = self.strategy.evaluate(income=1000, expenses=900)
        self.assertFalse(result["within_budget"])
        self.assertIn("overspending", result["recommendation"].lower())


class TestZeroBasedBudgetStrategy(unittest.TestCase):

    def setUp(self):
        self.strategy = ZeroBasedBudgetStrategy()

    def test_name(self):
        self.assertEqual(self.strategy.name(), "Zero-Based Budgeting")

    def test_balanced_budget(self):
        result = self.strategy.evaluate(income=1000, expenses=1000)
        self.assertTrue(result["balanced"])
        self.assertIn("perfectly balanced", result["recommendation"].lower())

    def test_surplus(self):
        result = self.strategy.evaluate(income=1000, expenses=800)
        self.assertFalse(result["balanced"])
        self.assertEqual(result["unallocated"], 200)
        self.assertIn("unallocated", result["recommendation"].lower())

    def test_overspending(self):
        result = self.strategy.evaluate(income=1000, expenses=1200)
        self.assertFalse(result["balanced"])
        self.assertIn("overspending", result["recommendation"].lower())


class TestBudgetPlanner(unittest.TestCase):

    def test_strategy_swap_at_runtime(self):
        planner = BudgetPlanner(FiftyThirtyTwentyStrategy())
        self.assertEqual(planner.get_strategy_name(), "50/30/20 Rule")

        result1 = planner.evaluate(income=1000, expenses=700)
        self.assertTrue(result1["within_budget"])

        # Swap strategy at runtime
        planner.strategy = ZeroBasedBudgetStrategy()
        self.assertEqual(planner.get_strategy_name(), "Zero-Based Budgeting")

        result2 = planner.evaluate(income=1000, expenses=700)
        self.assertFalse(result2["balanced"])

    def test_evaluate_delegates_to_strategy(self):
        planner = BudgetPlanner(ZeroBasedBudgetStrategy())
        result = planner.evaluate(income=500, expenses=500)
        self.assertTrue(result["balanced"])


if __name__ == "__main__":
    unittest.main()
