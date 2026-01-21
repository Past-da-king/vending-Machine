"""
Inventory management for the vending machine.
Handles stock levels and product availability.
"""
from typing import Dict, Optional, List
from .drinks import Drink


class Inventory:
    """
    Manages the stock of drinks in the vending machine.
    
    Provides methods for adding, checking, and updating stock levels.
    Implements the Single Responsibility Principle by focusing only
    on inventory management.
    """
    
    def __init__(self):
        """Initialize an empty inventory."""
        self._stock: Dict[str, dict] = {}  # code -> {'drink': Drink, 'quantity': int}
    
    def add_item(self, drink: Drink, quantity: int) -> None:
        """
        Add a drink to the inventory.
        
        Args:
            drink: The drink to add
            quantity: Initial stock quantity
            
        Raises:
            ValueError: If quantity is negative
        """
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")
        
        self._stock[drink.code] = {
            'drink': drink,
            'quantity': quantity
        }
    
    def get_item(self, code: str) -> Optional[Drink]:
        """
        Get a drink by its code.
        
        Args:
            code: The product code
            
        Returns:
            The Drink object if found, None otherwise
        """
        item = self._stock.get(code)
        return item['drink'] if item else None
    
    def has_stock(self, code: str) -> bool:
        """
        Check if an item is in stock.
        
        Args:
            code: The product code
            
        Returns:
            True if the item exists and has quantity > 0
        """
        item = self._stock.get(code)
        return item is not None and item['quantity'] > 0
    
    def get_quantity(self, code: str) -> int:
        """
        Get the stock quantity for a product.
        
        Args:
            code: The product code
            
        Returns:
            The quantity in stock, or 0 if not found
        """
        item = self._stock.get(code)
        return item['quantity'] if item else 0
    
    def decrement_stock(self, code: str) -> bool:
        """
        Decrease stock by 1 after a purchase.
        
        Args:
            code: The product code
            
        Returns:
            True if successful, False if out of stock or not found
        """
        if not self.has_stock(code):
            return False
        self._stock[code]['quantity'] -= 1
        return True
    
    def restock(self, code: str, quantity: int) -> bool:
        """
        Add stock to an existing item.
        
        Args:
            code: The product code
            quantity: Amount to add
            
        Returns:
            True if successful, False if item not found
        """
        if code not in self._stock:
            return False
        if quantity < 0:
            raise ValueError("Restock quantity cannot be negative")
        self._stock[code]['quantity'] += quantity
        return True
    
    def get_all_items(self) -> Dict[str, dict]:
        """
        Get all items with their details.
        
        Returns:
            Dictionary of all stock items
        """
        return {
            code: {
                'name': data['drink'].name,
                'price': data['drink'].price,
                'quantity': data['quantity'],
                'category': data['drink'].get_category(),
                'description': data['drink'].get_description()
            }
            for code, data in self._stock.items()
        }
    
    def get_available_items(self) -> List[Drink]:
        """
        Get all drinks that are currently in stock.
        
        Returns:
            List of available Drink objects
        """
        return [
            data['drink']
            for data in self._stock.values()
            if data['quantity'] > 0
        ]
    
    def __len__(self) -> int:
        """Return the total number of unique products."""
        return len(self._stock)
