"""
CLI Menu handler for the vending machine.
Manages user interaction flow.
"""
from typing import Optional
from .display import Display
from .admin import AdminHandler
from ..core import VendingMachine
from ..utils import InvalidAmountError


class MenuHandler:
    """
    Handles the CLI menu system.
    
    Provides a clean interface for user interaction with the vending machine.
    """
    
    def __init__(self, machine: VendingMachine):
        """
        Initialize the menu handler.
        
        Args:
            machine: The vending machine to control
        """
        self._machine = machine
        self._running = True
        self._admin = AdminHandler(machine)
    
    def run(self) -> None:
        """Run the main menu loop."""
        Display.display_welcome()
        
        while self._running:
            Display.display_options()
            choice = input("\nEnter choice (1-7): ").strip()
            
            if choice == '1':
                self._show_menu()
            elif choice == '2':
                self._insert_money()
            elif choice == '3':
                self._select_item()
            elif choice == '4':
                self._show_statistics()
            elif choice == '5':
                self._refund_and_exit()
            elif choice == '6':
                self._admin_mode()
            elif choice == '7':
                self._quit()
            else:
                Display.print_error("Invalid choice. Please enter 1-7.")
    
    def _show_menu(self) -> None:
        """Display the product menu."""
        items = self._machine.get_menu()
        Display.display_menu(items, self._machine.balance)
    
    def _insert_money(self) -> None:
        """Handle money insertion."""
        try:
            amount_str = input("Enter amount to insert: $").strip()
            amount = float(amount_str)
            new_balance = self._machine.insert_money(amount)
            Display.print_success(f"Inserted ${amount:.2f}. New balance: ${new_balance:.2f}")
        except ValueError:
            Display.print_error("Please enter a valid number.")
        except InvalidAmountError as e:
            Display.print_error(str(e))
    
    def _select_item(self) -> None:
        """Handle item selection."""
        # Show menu first
        self._show_menu()
        
        code = input("\nEnter product code: ").strip().upper()
        success, message, transaction = self._machine.select_item(code)
        
        if success:
            Display.print_success(message)
            if transaction:
                drink = self._machine.inventory.get_item(code)
                desc = drink.get_description() if drink else ""
                Display.display_receipt(transaction, desc)
        else:
            Display.print_error(message)
    
    def _show_statistics(self) -> None:
        """Display transaction statistics."""
        stats = self._machine.get_statistics()
        Display.display_statistics(stats)
    
    def _refund_and_exit(self) -> None:
        """Refund money and exit."""
        refund = self._machine.refund()
        if refund > 0:
            Display.print_info(f"Refunding ${refund:.2f}")
        Display.print_info("Thank you for using our vending machine. Goodbye!")
        self._running = False
    
    def _admin_mode(self) -> None:
        """Enter admin mode."""
        self._admin.run()
    
    def _quit(self) -> None:
        """Quit without refund."""
        Display.print_info("Goodbye!")
        self._running = False

