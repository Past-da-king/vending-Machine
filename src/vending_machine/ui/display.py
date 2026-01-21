"""
Display utilities for the CLI interface.
Provides formatted output for a professional user experience.
"""
from typing import Dict, List, Any
import os


class Display:
    """
    Utility class for displaying formatted output.
    
    Provides static methods for consistent, professional CLI presentation.
    """
    
    @staticmethod
    def print_header(title: str, width: int = 60) -> None:
        """Print a formatted header."""
        print("\n" + "=" * width)
        print(f"{title:^{width}}")
        print("=" * width)
    
    @staticmethod
    def print_section(title: str) -> None:
        """Print a section header."""
        print(f"\n{title}")
        print("-" * len(title))
    
    @staticmethod
    def print_success(message: str) -> None:
        """Print a success message."""
        print(f"[SUCCESS] {message}")
    
    @staticmethod
    def print_error(message: str) -> None:
        """Print an error message."""
        print(f"[ERROR] {message}")
    
    @staticmethod
    def print_warning(message: str) -> None:
        """Print a warning message."""
        print(f"[WARNING] {message}")
    
    @staticmethod
    def print_info(message: str) -> None:
        """Print an informational message."""
        print(f"[INFO] {message}")
    
    @staticmethod
    def display_menu(items: Dict[str, Any], balance: float) -> None:
        """
        Display the vending machine menu.
        
        Args:
            items: Dictionary of items from inventory
            balance: Current user balance
        """
        Display.print_header("VENDING MACHINE MENU")
        print(f"\nYour Balance: ${balance:.2f}\n")
        
        headers = ["Code", "Name", "Price", "Stock", "Status"]
        print(f"{'Code':<6} | {'Name':<18} | {'Price':<8} | {'Stock':<6} | {'Status'}")
        print("-" * 60)
        
        for code, details in items.items():
            status = "Available" if details['quantity'] > 0 else "OUT OF STOCK"
            print(
                f"{code:<6} | "
                f"{details['name']:<18} | "
                f"${details['price']:<7.2f} | "
                f"{details['quantity']:<6} | "
                f"{status}"
            )
    
    @staticmethod
    def display_receipt(transaction: Dict, drink_desc: str = "") -> None:
        """
        Display a purchase receipt.
        
        Args:
            transaction: Transaction dictionary
            drink_desc: Optional drink description
        """
        Display.print_header("RECEIPT")
        
        print(f"Transaction ID: {transaction.get('id', 'N/A')}")
        print(f"Time: {transaction.get('timestamp', 'N/A')[:19]}")
        print(f"\nItem: {transaction.get('item_name', 'N/A')}")
        if drink_desc:
            print(f"Description: {drink_desc}")
        print(f"\nPrice: ${transaction.get('item_price', 0):.2f}")
        print(f"Paid: ${transaction.get('amount_paid', 0):.2f}")
        print(f"Change: ${transaction.get('change_given', 0):.2f}")
        print(f"\nStatus: {transaction.get('status', 'N/A')}")
        print("\nThank you for your purchase!")
        print("=" * 60)
    
    @staticmethod
    def display_statistics(stats: Dict) -> None:
        """Display transaction statistics."""
        Display.print_header("TRANSACTION STATISTICS")
        
        print(f"Total Transactions: {stats.get('total_transactions', 0)}")
        print(f"Successful: {stats.get('successful', 0)}")
        print(f"Failed: {stats.get('failed', 0)}")
        print(f"Success Rate: {stats.get('success_rate', 0):.1f}%")
        print(f"Total Revenue: ${stats.get('total_revenue', 0):.2f}")
    
    @staticmethod
    def display_welcome() -> None:
        """Display welcome message."""
        Display.print_header("VENDING MACHINE SIMULATOR", 60)
        print("A modular, object-oriented simulation")
        print("Demonstrating SOLID principles and clean architecture")
        print("=" * 60)
    
    @staticmethod
    def display_options() -> None:
        """Display available options."""
        Display.print_section("OPTIONS")
        print("1. View Menu")
        print("2. Insert Money")
        print("3. Select Item")
        print("4. View Statistics")
        print("5. Refund & Exit")
        print("6. Admin Mode")
        print("7. Quit")
    
    @staticmethod
    def clear_screen() -> None:
        """Clear the console screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def print_divider(char: str = "-", length: int = 60) -> None:
        """Print a divider line."""
        print(char * length)
