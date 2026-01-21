"""
Payment service abstraction.
Implements the Dependency Inversion Principle for payment processing.
"""
from abc import ABC, abstractmethod
from typing import Tuple


class PaymentService(ABC):
    """
    Abstract base class for payment processing.
    
    Allows the vending machine to work with different payment methods
    without being coupled to a specific implementation.
    """
    
    @abstractmethod
    def insert_money(self, amount: float) -> bool:
        """Insert money into the machine."""
        pass
    
    @abstractmethod
    def get_balance(self) -> float:
        """Get the current balance."""
        pass
    
    @abstractmethod
    def deduct(self, amount: float) -> Tuple[bool, float]:
        """Deduct an amount and return success status and remaining balance."""
        pass
    
    @abstractmethod
    def refund(self) -> float:
        """Refund all money and return the amount."""
        pass


class CashPaymentService(PaymentService):
    """
    Cash-based payment service implementation.
    
    Handles cash transactions with proper validation and change calculation.
    """
    
    def __init__(self):
        self._balance: float = 0.0
    
    def insert_money(self, amount: float) -> bool:
        """
        Insert cash into the machine.
        
        Args:
            amount: Amount to insert
            
        Returns:
            True if successful
            
        Raises:
            ValueError: If amount is not positive
        """
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self._balance += amount
        return True
    
    def get_balance(self) -> float:
        """Get the current cash balance."""
        return self._balance
    
    def deduct(self, amount: float) -> Tuple[bool, float]:
        """
        Deduct amount from balance.
        
        Args:
            amount: Amount to deduct
            
        Returns:
            Tuple of (success, change_amount)
        """
        if amount > self._balance:
            return False, 0.0
        
        change = self._balance - amount
        self._balance = 0.0
        return True, change
    
    def refund(self) -> float:
        """Refund all inserted money."""
        refund_amount = self._balance
        self._balance = 0.0
        return refund_amount
