# transaction_adapter.py

from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory


class TransactionAdapter:
    """
    Adapter Pattern: Converts an external freelance income transaction
    (with invoice ID and project details) into a standard Transaction object
    compatible with the application's internal interface.
    """

    def __init__(self, external_transaction):
        self.external_transaction = external_transaction

    def to_transaction(self):
        """Convert an external transaction to a standard Transaction."""
        return Transaction(
            amount=self.external_transaction.amount,
            category=TransactionCategory.INCOME
        )
