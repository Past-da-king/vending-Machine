"""
Integration tests for the Vending Machine system.
Tests complete workflows end-to-end.
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from vending_machine.models import Inventory, Soda, Juice, Water
from vending_machine.core import VendingMachine


class TestCompletePurchaseWorkflow(unittest.TestCase):
    """Test complete purchase scenarios."""
    
    def setUp(self):
        self.inventory = Inventory()
        self.inventory.add_item(Soda("A1", "Cola", 1.50), 3)
        self.inventory.add_item(Juice("B1", "OJ", 2.00), 2)
        self.inventory.add_item(Water("C1", "Water", 1.00), 5)
        self.machine = VendingMachine(self.inventory)
    
    def test_single_purchase_workflow(self):
        """Test a complete single item purchase."""
        # Insert money
        self.machine.insert_money(2.00)
        self.assertEqual(self.machine.balance, 2.00)
        
        # Make purchase
        success, message, txn = self.machine.select_item("A1")
        
        # Verify results
        self.assertTrue(success)
        self.assertEqual(self.machine.balance, 0.0)
        self.assertEqual(self.inventory.get_quantity("A1"), 2)
        self.assertIsNotNone(txn)
    
    def test_multiple_purchases_workflow(self):
        """Test multiple sequential purchases."""
        # First purchase
        self.machine.insert_money(2.00)
        success1, _, _ = self.machine.select_item("A1")
        
        # Second purchase
        self.machine.insert_money(1.00)
        success2, _, _ = self.machine.select_item("C1")
        
        # Verify
        self.assertTrue(success1)
        self.assertTrue(success2)
        self.assertEqual(self.inventory.get_quantity("A1"), 2)
        self.assertEqual(self.inventory.get_quantity("C1"), 4)
    
    def test_partial_funds_then_complete(self):
        """Test inserting money in stages before purchase."""
        self.machine.insert_money(0.50)
        self.machine.insert_money(0.50)
        self.machine.insert_money(0.50)
        
        success, _, _ = self.machine.select_item("A1")
        
        self.assertTrue(success)


class TestDepletionWorkflow(unittest.TestCase):
    """Test stock depletion scenarios."""
    
    def setUp(self):
        self.inventory = Inventory()
        self.inventory.add_item(Soda("A1", "Cola", 1.00), 2)  # Only 2 in stock
        self.machine = VendingMachine(self.inventory)
    
    def test_deplete_stock(self):
        """Test buying until out of stock."""
        # Buy first
        self.machine.insert_money(1.00)
        success1, _, _ = self.machine.select_item("A1")
        
        # Buy second
        self.machine.insert_money(1.00)
        success2, _, _ = self.machine.select_item("A1")
        
        # Third should fail
        self.machine.insert_money(1.00)
        success3, message3, _ = self.machine.select_item("A1")
        
        self.assertTrue(success1)
        self.assertTrue(success2)
        self.assertFalse(success3)
        self.assertIn("out of stock", message3.lower())


class TestStatisticsWorkflow(unittest.TestCase):
    """Test statistics accumulation."""
    
    def setUp(self):
        self.inventory = Inventory()
        self.inventory.add_item(Soda("A1", "Cola", 1.50), 5)
        self.inventory.add_item(Water("C1", "Water", 1.00), 5)
        self.machine = VendingMachine(self.inventory)
    
    def test_statistics_after_transactions(self):
        """Statistics should reflect all transactions."""
        # Successful purchases
        self.machine.insert_money(2.00)
        self.machine.select_item("A1")
        
        self.machine.insert_money(1.00)
        self.machine.select_item("C1")
        
        # Failed purchase (insufficient funds)
        self.machine.insert_money(0.50)
        self.machine.select_item("A1")
        
        stats = self.machine.get_statistics()
        
        self.assertEqual(stats['total_transactions'], 3)
        self.assertEqual(stats['successful'], 2)
        self.assertEqual(stats['failed'], 1)
        self.assertEqual(stats['total_revenue'], 2.50)


class TestRefundWorkflow(unittest.TestCase):
    """Test refund scenarios."""
    
    def setUp(self):
        self.inventory = Inventory()
        self.inventory.add_item(Soda("A1", "Cola", 1.50), 5)
        self.machine = VendingMachine(self.inventory)
    
    def test_refund_before_purchase(self):
        """Should be able to refund without buying."""
        self.machine.insert_money(5.00)
        refund = self.machine.refund()
        
        self.assertEqual(refund, 5.00)
        self.assertEqual(self.machine.balance, 0.0)
    
    def test_refund_after_failed_purchase(self):
        """Refund should work after failed purchase."""
        self.machine.insert_money(1.00)  # Not enough for Cola
        self.machine.select_item("A1")   # Fails
        
        refund = self.machine.refund()
        
        self.assertEqual(refund, 1.00)


if __name__ == '__main__':
    unittest.main(verbosity=2)
