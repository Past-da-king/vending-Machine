"""
Unit tests for the VendingMachine core class.
Tests the main controller orchestration.
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from vending_machine.models import Inventory, Soda, Juice, Water
from vending_machine.core import VendingMachine
from vending_machine.utils import InvalidAmountError


class TestVendingMachineBasics(unittest.TestCase):
    """Test basic vending machine operations."""
    
    def setUp(self):
        self.inventory = Inventory()
        self.inventory.add_item(Soda("A1", "Cola", 1.50), 5)
        self.inventory.add_item(Water("C1", "Water", 1.00), 3)
        self.machine = VendingMachine(self.inventory)
    
    def test_initial_balance_is_zero(self):
        """Machine should start with zero balance."""
        self.assertEqual(self.machine.balance, 0.0)
    
    def test_insert_money(self):
        """insert_money should increase balance."""
        self.machine.insert_money(1.00)
        self.assertEqual(self.machine.balance, 1.00)
    
    def test_insert_money_returns_new_balance(self):
        """insert_money should return new balance."""
        result = self.machine.insert_money(2.50)
        self.assertEqual(result, 2.50)
    
    def test_insert_negative_raises_error(self):
        """Inserting negative amount should raise InvalidAmountError."""
        with self.assertRaises(InvalidAmountError):
            self.machine.insert_money(-1.00)
    
    def test_insert_zero_raises_error(self):
        """Inserting zero should raise InvalidAmountError."""
        with self.assertRaises(InvalidAmountError):
            self.machine.insert_money(0)


class TestVendingMachinePurchase(unittest.TestCase):
    """Test purchase functionality."""
    
    def setUp(self):
        self.inventory = Inventory()
        self.inventory.add_item(Soda("A1", "Cola", 1.50), 2)
        self.inventory.add_item(Water("C1", "Water", 1.00), 1)
        self.machine = VendingMachine(self.inventory)
    
    def test_successful_purchase(self):
        """Should successfully purchase with sufficient funds."""
        self.machine.insert_money(2.00)
        success, message, txn = self.machine.select_item("A1")
        
        self.assertTrue(success)
        self.assertIn("Dispensing", message)
        self.assertIn("Cola", message)
    
    def test_purchase_returns_change(self):
        """Successful purchase should show correct change."""
        self.machine.insert_money(2.00)
        success, message, txn = self.machine.select_item("A1")
        
        self.assertIn("$0.50", message)
    
    def test_purchase_decrements_stock(self):
        """Successful purchase should reduce stock."""
        self.machine.insert_money(2.00)
        self.machine.select_item("A1")
        
        self.assertEqual(self.inventory.get_quantity("A1"), 1)
    
    def test_purchase_resets_balance(self):
        """Successful purchase should reset balance to zero."""
        self.machine.insert_money(2.00)
        self.machine.select_item("A1")
        
        self.assertEqual(self.machine.balance, 0.0)
    
    def test_purchase_returns_transaction(self):
        """Successful purchase should return transaction dict."""
        self.machine.insert_money(2.00)
        success, message, txn = self.machine.select_item("A1")
        
        self.assertIsNotNone(txn)
        self.assertIn("id", txn)
        self.assertEqual(txn["item_name"], "Cola")


class TestVendingMachineFailures(unittest.TestCase):
    """Test failure scenarios."""
    
    def setUp(self):
        self.inventory = Inventory()
        self.inventory.add_item(Soda("A1", "Cola", 1.50), 1)
        self.machine = VendingMachine(self.inventory)
    
    def test_insufficient_funds(self):
        """Should fail with insufficient funds."""
        self.machine.insert_money(1.00)
        success, message, txn = self.machine.select_item("A1")
        
        self.assertFalse(success)
        self.assertIn("Insufficient", message)
    
    def test_insufficient_funds_keeps_balance(self):
        """Failed purchase should keep balance intact."""
        self.machine.insert_money(1.00)
        self.machine.select_item("A1")
        
        self.assertEqual(self.machine.balance, 1.00)
    
    def test_out_of_stock(self):
        """Should fail when item out of stock."""
        # Deplete stock
        self.machine.insert_money(2.00)
        self.machine.select_item("A1")
        
        # Try again
        self.machine.insert_money(2.00)
        success, message, txn = self.machine.select_item("A1")
        
        self.assertFalse(success)
        self.assertIn("out of stock", message.lower())
    
    def test_invalid_product_code(self):
        """Should fail with invalid product code."""
        self.machine.insert_money(5.00)
        success, message, txn = self.machine.select_item("Z9")
        
        self.assertFalse(success)
        self.assertIn("Invalid", message)


class TestVendingMachineRefund(unittest.TestCase):
    """Test refund functionality."""
    
    def setUp(self):
        self.inventory = Inventory()
        self.inventory.add_item(Soda("A1", "Cola", 1.50), 5)
        self.machine = VendingMachine(self.inventory)
    
    def test_refund_returns_balance(self):
        """refund should return full balance."""
        self.machine.insert_money(2.50)
        refund = self.machine.refund()
        
        self.assertEqual(refund, 2.50)
    
    def test_refund_resets_balance(self):
        """refund should reset balance to zero."""
        self.machine.insert_money(2.50)
        self.machine.refund()
        
        self.assertEqual(self.machine.balance, 0.0)
    
    def test_refund_empty_balance(self):
        """refund with no money should return 0."""
        refund = self.machine.refund()
        self.assertEqual(refund, 0.0)


class TestVendingMachineStatistics(unittest.TestCase):
    """Test statistics functionality."""
    
    def setUp(self):
        self.inventory = Inventory()
        self.inventory.add_item(Soda("A1", "Cola", 1.50), 5)
        self.inventory.add_item(Water("C1", "Water", 1.00), 5)
        self.machine = VendingMachine(self.inventory)
    
    def test_get_statistics(self):
        """get_statistics should return stats dict."""
        # Make some transactions
        self.machine.insert_money(2.00)
        self.machine.select_item("A1")
        
        self.machine.insert_money(1.00)
        self.machine.select_item("C1")
        
        stats = self.machine.get_statistics()
        
        self.assertEqual(stats['successful'], 2)
        self.assertEqual(stats['total_revenue'], 2.50)


if __name__ == '__main__':
    unittest.main(verbosity=2)
