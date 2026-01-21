"""
Admin menu handler for the vending machine.
Provides administrative functions for managing the machine.
"""
from typing import Optional
from .display import Display
from ..core import VendingMachine
from ..models import Soda, Juice, Water


class AdminHandler:
    """
    Handles the admin menu system.
    
    Provides administrative functions for inventory management,
    transaction viewing, and machine maintenance.
    """
    
    # Simple admin password (in production, use proper authentication)
    ADMIN_PASSWORD = "admin123"
    
    def __init__(self, machine: VendingMachine):
        """
        Initialize the admin handler.
        
        Args:
            machine: The vending machine to manage
        """
        self._machine = machine
        self._authenticated = False
    
    def authenticate(self) -> bool:
        """
        Authenticate the admin user.
        
        Returns:
            True if authentication successful
        """
        password = input("Enter admin password: ").strip()
        if password == self.ADMIN_PASSWORD:
            self._authenticated = True
            Display.print_success("Authentication successful!")
            return True
        else:
            Display.print_error("Invalid password!")
            return False
    
    def run(self) -> None:
        """Run the admin menu loop."""
        if not self._authenticated:
            if not self.authenticate():
                return
        
        Display.print_header("ADMIN PANEL")
        
        while True:
            self._display_admin_options()
            choice = input("\nEnter choice (1-6): ").strip()
            
            if choice == '1':
                self._view_inventory()
            elif choice == '2':
                self._restock_item()
            elif choice == '3':
                self._view_transactions()
            elif choice == '4':
                self._view_statistics()
            elif choice == '5':
                self._add_new_item()
            elif choice == '6':
                Display.print_info("Exiting admin panel...")
                break
            else:
                Display.print_error("Invalid choice. Please enter 1-6.")
    
    def _display_admin_options(self) -> None:
        """Display admin menu options."""
        Display.print_section("ADMIN OPTIONS")
        print("1. View Inventory")
        print("2. Restock Item")
        print("3. View Transactions")
        print("4. View Statistics")
        print("5. Add New Item")
        print("6. Exit Admin Panel")
    
    def _view_inventory(self) -> None:
        """Display full inventory details."""
        Display.print_header("INVENTORY MANAGEMENT")
        items = self._machine.get_menu()
        
        if not items:
            Display.print_warning("Inventory is empty!")
            return
        
        print(f"\n{'Code':<6} | {'Name':<18} | {'Price':<8} | {'Qty':<5} | {'Category':<10} | {'Description'}")
        print("-" * 85)
        
        for code, details in items.items():
            print(
                f"{code:<6} | "
                f"{details['name']:<18} | "
                f"${details['price']:<7.2f} | "
                f"{details['quantity']:<5} | "
                f"{details['category']:<10} | "
                f"{details['description']}"
            )
        
        print("-" * 85)
        print(f"Total unique products: {len(items)}")
    
    def _restock_item(self) -> None:
        """Restock an existing item."""
        self._view_inventory()
        
        code = input("\nEnter item code to restock: ").strip().upper()
        
        if not self._machine.inventory.get_item(code):
            Display.print_error(f"Item {code} not found!")
            return
        
        try:
            quantity = int(input("Enter quantity to add: ").strip())
            if quantity <= 0:
                Display.print_error("Quantity must be positive!")
                return
            
            success = self._machine.inventory.restock(code, quantity)
            if success:
                new_qty = self._machine.inventory.get_quantity(code)
                Display.print_success(f"Restocked {code}. New quantity: {new_qty}")
            else:
                Display.print_error("Failed to restock item!")
        except ValueError:
            Display.print_error("Please enter a valid number!")
    
    def _view_transactions(self) -> None:
        """Display all transactions."""
        Display.print_header("TRANSACTION HISTORY")
        
        transactions = self._machine.transactions.get_all()
        
        if not transactions:
            Display.print_warning("No transactions recorded yet.")
            return
        
        print(f"\n{'ID':<12} | {'Time':<20} | {'Item':<15} | {'Price':<8} | {'Paid':<8} | {'Change':<8} | {'Status'}")
        print("-" * 95)
        
        for txn in transactions:
            timestamp = txn.get('timestamp', 'N/A')[:19]
            print(
                f"{txn.get('id', 'N/A'):<12} | "
                f"{timestamp:<20} | "
                f"{txn.get('item_name', 'N/A'):<15} | "
                f"${txn.get('item_price', 0):<7.2f} | "
                f"${txn.get('amount_paid', 0):<7.2f} | "
                f"${txn.get('change_given', 0):<7.2f} | "
                f"{txn.get('status', 'N/A')}"
            )
        
        print("-" * 95)
        print(f"Total transactions: {len(transactions)}")
    
    def _view_statistics(self) -> None:
        """Display detailed statistics."""
        stats = self._machine.get_statistics()
        Display.display_statistics(stats)
        
        # Extra admin stats
        print("\n--- Inventory Summary ---")
        items = self._machine.get_menu()
        total_stock = sum(details['quantity'] for details in items.values())
        out_of_stock = sum(1 for details in items.values() if details['quantity'] == 0)
        
        print(f"Total items in stock: {total_stock}")
        print(f"Products out of stock: {out_of_stock}")
        print(f"Unique products: {len(items)}")
    
    def _add_new_item(self) -> None:
        """Add a new item to the inventory."""
        Display.print_header("ADD NEW ITEM")
        
        print("\nSelect drink type:")
        print("1. Soda")
        print("2. Juice")
        print("3. Water")
        
        drink_type = input("Enter choice (1-3): ").strip()
        
        try:
            code = input("Enter product code (e.g., D1): ").strip().upper()
            
            if self._machine.inventory.get_item(code):
                Display.print_error(f"Item with code {code} already exists!")
                return
            
            name = input("Enter product name: ").strip()
            price = float(input("Enter price: $").strip())
            quantity = int(input("Enter initial stock quantity: ").strip())
            
            if price <= 0 or quantity < 0:
                Display.print_error("Price must be positive and quantity non-negative!")
                return
            
            # Create drink based on type
            if drink_type == '1':
                is_diet = input("Is it diet? (y/n): ").strip().lower() == 'y'
                drink = Soda(code, name, price, is_diet=is_diet)
            elif drink_type == '2':
                fruit = input("Enter fruit type (e.g., Orange): ").strip()
                drink = Juice(code, name, price, fruit_type=fruit)
            elif drink_type == '3':
                is_sparkling = input("Is it sparkling? (y/n): ").strip().lower() == 'y'
                drink = Water(code, name, price, is_sparkling=is_sparkling)
            else:
                Display.print_error("Invalid drink type!")
                return
            
            self._machine.inventory.add_item(drink, quantity)
            Display.print_success(f"Added {name} ({code}) to inventory with {quantity} units!")
            
        except ValueError:
            Display.print_error("Invalid input! Please enter valid numbers for price and quantity.")
