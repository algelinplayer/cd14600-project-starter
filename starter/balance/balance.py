# balance.py

from transaction.transaction_category import TransactionCategory


class Balance:
    """Singleton to track the balance."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        """Enforce Singleton: only one instance can exist."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._balance = 0.0
            cls._instance._observers = []
        return cls._instance

    def __init__(self):
        """Initialize the balance. Prevent direct instantiation."""
        pass

    @classmethod
    def get_instance(cls):
        """Return the single Balance instance, creating it if needed."""
        if cls._instance is None:
            cls()
        return cls._instance

    def reset(self):
        """Reset the net balance to zero."""
        self._balance = 0.0
        self._observers = []

    def register_observer(self, observer):
        """Register an observer to be notified on balance changes."""
        if observer not in self._observers:
            self._observers.append(observer)

    def unregister_observer(self, observer):
        """Remove an observer from the notification list."""
        if observer in self._observers:
            self._observers.remove(observer)

    def _notify_observers(self, transaction):
        """Notify all registered observers of a balance change."""
        for observer in self._observers:
            observer.update(self._balance, transaction)

    def add_income(self, amount):
        """Add income to the balance."""
        self._balance += amount

    def add_expense(self, amount):
        """Subtract expense from the balance."""
        self._balance -= amount

    def apply_transaction(self, transaction):
        """
        Apply a Transaction object to update the balance.

        Args:
            transaction (Transaction): The transaction to apply.
        """
        if transaction.category == TransactionCategory.INCOME:
            self.add_income(transaction.amount)
        elif transaction.category == TransactionCategory.EXPENSE:
            self.add_expense(transaction.amount)
        else:
            raise ValueError(f"Unknown transaction category: {transaction.category}")
        self._notify_observers(transaction)

    def get_balance(self):
        """Get the current net balance."""
        return self._balance

    def summary(self):
        """Return a summary string of the net balance."""
        return f"Current Balance: ${self._balance:.2f}"
