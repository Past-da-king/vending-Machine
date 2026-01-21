#!/usr/bin/env python3
"""
Unit tests for cash-out functionality.
Tests the VendingMachine's cash reserve tracking and cash-out operations.
"""
import unittest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from vending_machine.models import Inventory, Soda, Juice
from vending_machine.core import VendingMachine


class TestCashOut(unittest.TestCase):
    """Test cash-out and cash reserve functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.inventory = Inventory()
        self.inventory.add_item(Soda("A1", "Coke", 1.50), 5)
        self.inventory.add_item(Juice("B1", "Orange Juice", 2.00, "Orange"), 3)
        self.machine = VendingMachine(self.inventory)
    
    def test_initial_cash_reserve_is_zero(self):
        """Test that a new vending machine has zero cash reserve."""
        self.assertEqual(self.machine.cash_reserve, 0.0)
    
    def test_successful_purchase_adds_to_cash_reserve(self):
        """Test that successful purchases add to the cash reserve."""
        self.machine.insert_money(2.00)
        success, message, _ = self.machine.select_item("A1")
        
        self.assertTrue(success)
        self.assertEqual(self.machine.cash_reserve, 1.50)
    
    def test_failed_purchase_does_not_add_to_cash_reserve(self):
        """Test that failed purchases don't affect cash reserve."""
        # Try to buy without money
        success, message, _ = self.machine.select_item("A1")
        
        self.assertFalse(success)
        self.assertEqual(self.machine.cash_reserve, 0.0)
    
    def test_multiple_purchases_accumulate_correctly(self):
        """Test that multiple purchases accumulate in cash reserve."""
        # Purchase 1: Coke for $1.50
        self.machine.insert_money(2.00)
        self.machine.select_item("A1")
        
        # Purchase 2: Orange Juice for $2.00
        self.machine.insert_money(3.00)
        self.machine.select_item("B1")
        
        # Total should be $1.50 + $2.00 = $3.50
        self.assertEqual(self.machine.cash_reserve, 3.50)
    
    def test_cash_out_returns_correct_amount(self):
        """Test that cash_out returns the correct amount."""
        # Make some purchases
        self.machine.insert_money(5.00)
        self.machine.select_item("A1")  # $1.50
        self.machine.insert_money(5.00)
        self.machine.select_item("B1")  # $2.00
        
        # Cash out
        cashed_out = self.machine.cash_out()
        
        self.assertEqual(cashed_out, 3.50)
    
    def test_cash_out_resets_to_zero(self):
        """Test that cash_out resets the cash reserve to zero."""
        # Make purchases
        self.machine.insert_money(2.00)
        self.machine.select_item("A1")
        
        # Verify there's cash
        self.assertGreater(self.machine.cash_reserve, 0)
        
        # Cash out
        self.machine.cash_out()
        
        # Verify reset to zero
        self.assertEqual(self.machine.cash_reserve, 0.0)
    
    def test_cash_out_when_empty(self):
        """Test cash_out when there's no cash in the machine."""
        cashed_out = self.machine.cash_out()
        
        self.assertEqual(cashed_out, 0.0)
        self.assertEqual(self.machine.cash_reserve, 0.0)
    
    def test_cash_reserve_after_cash_out_and_new_purchase(self):
        """Test that cash reserve correctly accumulates after a cash-out."""
        # Make purchase
        self.machine.insert_money(2.00)
        self.machine.select_item("A1")  # $1.50
        
        # Cash out
        self.machine.cash_out()
        self.assertEqual(self.machine.cash_reserve, 0.0)
        
        # Make new purchase
        self.machine.insert_money(3.00)
        self.machine.select_item("B1")  # $2.00
        
        # Should only have the new purchase amount
        self.assertEqual(self.machine.cash_reserve, 2.00)
    
    def test_out_of_stock_does_not_add_to_cash_reserve(self):
        """Test that out-of-stock purchases don't add to cash reserve."""
        # Empty the stock
        for _ in range(5):
            self.machine.insert_money(2.00)
            self.machine.select_item("A1")
        
        initial_reserve = self.machine.cash_reserve
        
        # Try to buy when out of stock
        self.machine.insert_money(2.00)
        success, _, _ = self.machine.select_item("A1")
        
        self.assertFalse(success)
        self.assertEqual(self.machine.cash_reserve, initial_reserve)


if __name__ == '__main__':
    unittest.main()
