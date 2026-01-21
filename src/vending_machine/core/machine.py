"""
Core VendingMachine controller.
Orchestrates interactions between inventory, payment, and transactions.
"""
from typing import Tuple, Optional, Dict

from ..models import Inventory, Drink
from ..services import CashPaymentService, TransactionService, PaymentService
from ..utils import (
    InsufficientFundsError,
    OutOfStockError,
    InvalidProductError,
    InvalidAmountError
)


class VendingMachine:
    """
    The main vending machine controller.
    
    Coordinates between inventory, payment processing, and transaction
    recording to provide a complete vending experience.
    
    Implements the Facade Pattern by providing a simple interface
    to a complex subsystem.
    """
    
    def __init__(
        self,
        inventory: Inventory,
        payment_service: Optional[PaymentService] = None,
        transaction_service: Optional[TransactionService] = None
    ):
        """
        Initialize the vending machine.
        
        Args:
            inventory: The inventory to use
            payment_service: Optional custom payment service (defaults to CashPaymentService)
            transaction_service: Optional custom transaction service
        """
        self._inventory = inventory
        self._payment = payment_service or CashPaymentService()
        self._transactions = transaction_service or TransactionService()
    
    @property
    def balance(self) -> float:
        """Get the current balance."""
        return self._payment.get_balance()
    
    @property
    def inventory(self) -> Inventory:
        """Get the inventory."""
        return self._inventory
    
    @property
    def transactions(self) -> TransactionService:
        """Get the transaction service."""
        return self._transactions
    
    def insert_money(self, amount: float) -> float:
        """
        Insert money into the machine.
        
        Args:
            amount: The amount to insert
            
        Returns:
            The new balance
            
        Raises:
            InvalidAmountError: If amount is not positive
        """
        if amount <= 0:
            raise InvalidAmountError(amount)
        self._payment.insert_money(amount)
        return self.balance
    
    def select_item(self, code: str) -> Tuple[bool, str, Optional[Dict]]:
        """
        Attempt to purchase an item.
        
        Args:
            code: The product code
            
        Returns:
            Tuple of (success, message, transaction_dict)
        """
        # Validate product exists
        drink = self._inventory.get_item(code)
        if not drink:
            return False, f"Invalid product code: {code}", None
        
        # Check stock
        if not self._inventory.has_stock(code):
            self._transactions.create_failed(
                code, drink.name, drink.price,
                self.balance, "Out of stock"
            )
            return False, f"{drink.name} is out of stock", None
        
        # Check funds
        if self.balance < drink.price:
            self._transactions.create_failed(
                code, drink.name, drink.price,
                self.balance, "Insufficient funds"
            )
            return (
                False,
                f"Insufficient funds. {drink.name} costs ${drink.price:.2f}, "
                f"but you only have ${self.balance:.2f}",
                None
            )
        
        # Process purchase
        success, change = self._payment.deduct(drink.price)
        if success:
            self._inventory.decrement_stock(code)
            txn = self._transactions.create_success(
                code, drink.name, drink.price,
                drink.price + change, change
            )
            return (
                True,
                f"Dispensing {drink.name}. Your change is ${change:.2f}",
                txn.to_dict()
            )
        
        return False, "Payment processing failed", None
    
    def refund(self) -> float:
        """
        Refund all inserted money.
        
        Returns:
            The amount refunded
        """
        return self._payment.refund()
    
    def get_menu(self) -> Dict[str, dict]:
        """Get all items formatted for display."""
        return self._inventory.get_all_items()
    
    def get_statistics(self) -> Dict:
        """Get transaction statistics."""
        return self._transactions.get_statistics()
