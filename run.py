#!/usr/bin/env python3
"""
Vending Machine Simulator - Entry Point

A comprehensive OOP simulation demonstrating SOLID principles
and clean architecture in Python.

Run with: python run.py
"""
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from vending_machine.models import Soda, Juice, Water, Inventory
from vending_machine.core import VendingMachine
from vending_machine.ui import MenuHandler


def create_default_inventory() -> Inventory:
    """
    Create the default inventory with sample drinks.
    
    Returns:
        Inventory: Stocked inventory ready for use
    """
    inventory = Inventory()
    
    # Add Sodas
    inventory.add_item(Soda("A1", "Coca-Cola", 1.50), 5)
    inventory.add_item(Soda("A2", "Pepsi", 1.50), 4)
    inventory.add_item(Soda("A3", "Diet Coke", 1.50, is_diet=True), 3)
    inventory.add_item(Soda("A4", "Sprite", 1.25), 6)
    
    # Add Juices
    inventory.add_item(Juice("B1", "Orange Juice", 2.00, fruit_type="Orange"), 3)
    inventory.add_item(Juice("B2", "Apple Juice", 2.00, fruit_type="Apple"), 3)
    inventory.add_item(Juice("B3", "Grape Juice", 2.25, fruit_type="Grape"), 2)
    
    # Add Waters
    inventory.add_item(Water("C1", "Spring Water", 1.00), 10)
    inventory.add_item(Water("C2", "Sparkling Water", 1.25, is_sparkling=True), 5)
    
    return inventory


def main():
    """Main entry point for the vending machine simulator."""
    try:
        # Initialize components
        inventory = create_default_inventory()
        machine = VendingMachine(inventory)
        menu = MenuHandler(machine)
        
        # Run the simulation
        menu.run()
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n[FATAL ERROR] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
