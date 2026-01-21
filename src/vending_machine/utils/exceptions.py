"""
Custom exceptions for the vending machine.
Provides domain-specific error handling.
"""


class VendingMachineError(Exception):
    """Base exception for vending machine errors."""
    pass


class InsufficientFundsError(VendingMachineError):
    """Raised when the user doesn't have enough money."""
    
    def __init__(self, required: float, available: float):
        self.required = required
        self.available = available
        super().__init__(
            f"Insufficient funds. Required: ${required:.2f}, Available: ${available:.2f}"
        )


class OutOfStockError(VendingMachineError):
    """Raised when a product is out of stock."""
    
    def __init__(self, product_name: str):
        self.product_name = product_name
        super().__init__(f"{product_name} is out of stock")


class InvalidProductError(VendingMachineError):
    """Raised when an invalid product code is used."""
    
    def __init__(self, code: str):
        self.code = code
        super().__init__(f"Invalid product code: {code}")


class InvalidAmountError(VendingMachineError):
    """Raised when an invalid amount is inserted."""
    
    def __init__(self, amount: float):
        self.amount = amount
        super().__init__(f"Invalid amount: ${amount:.2f}. Amount must be positive.")
