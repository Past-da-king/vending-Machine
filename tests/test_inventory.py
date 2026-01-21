"""
Unit tests for the Inventory class.
Tests stock management and product lookup.
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from vending_machine.models import Inventory, Soda, Juice, Water


class TestInventoryBasics(unittest.TestCase):
    """Test basic inventory operations."""
    
    def setUp(self):
        self.inventory = Inventory()
        self.cola = Soda("A1", "Cola", 1.50)
        self.water = Water("C1", "Water", 1.00)
    
    def test_empty_inventory(self):
        """New inventory should be empty."""
        self.assertEqual(len(self.inventory), 0)
    
    def test_add_item(self):
        """Adding an item should increase inventory size."""
        self.inventory.add_item(self.cola, 5)
        self.assertEqual(len(self.inventory), 1)
    
    def test_add_item_negative_quantity(self):
        """Adding item with negative quantity should raise error."""
        with self.assertRaises(ValueError):
            self.inventory.add_item(self.cola, -1)
    
    def test_get_item(self):
        """Should be able to retrieve added item."""
        self.inventory.add_item(self.cola, 5)
        retrieved = self.inventory.get_item("A1")
        self.assertEqual(retrieved.name, "Cola")
    
    def test_get_nonexistent_item(self):
        """Getting non-existent item should return None."""
        result = self.inventory.get_item("Z9")
        self.assertIsNone(result)


class TestInventoryStock(unittest.TestCase):
    """Test stock management operations."""
    
    def setUp(self):
        self.inventory = Inventory()
        self.cola = Soda("A1", "Cola", 1.50)
        self.inventory.add_item(self.cola, 3)
    
    def test_has_stock(self):
        """has_stock should return True for stocked items."""
        self.assertTrue(self.inventory.has_stock("A1"))
    
    def test_has_stock_empty(self):
        """has_stock should return False for empty stock."""
        # Deplete stock
        for _ in range(3):
            self.inventory.decrement_stock("A1")
        self.assertFalse(self.inventory.has_stock("A1"))
    
    def test_has_stock_nonexistent(self):
        """has_stock should return False for non-existent items."""
        self.assertFalse(self.inventory.has_stock("Z9"))
    
    def test_get_quantity(self):
        """get_quantity should return correct count."""
        self.assertEqual(self.inventory.get_quantity("A1"), 3)
    
    def test_get_quantity_nonexistent(self):
        """get_quantity should return 0 for non-existent items."""
        self.assertEqual(self.inventory.get_quantity("Z9"), 0)
    
    def test_decrement_stock(self):
        """decrement_stock should reduce quantity by 1."""
        self.inventory.decrement_stock("A1")
        self.assertEqual(self.inventory.get_quantity("A1"), 2)
    
    def test_decrement_stock_returns_true(self):
        """decrement_stock should return True on success."""
        result = self.inventory.decrement_stock("A1")
        self.assertTrue(result)
    
    def test_decrement_empty_stock_returns_false(self):
        """decrement_stock should return False when empty."""
        for _ in range(3):
            self.inventory.decrement_stock("A1")
        result = self.inventory.decrement_stock("A1")
        self.assertFalse(result)


class TestInventoryRestock(unittest.TestCase):
    """Test restocking operations."""
    
    def setUp(self):
        self.inventory = Inventory()
        self.cola = Soda("A1", "Cola", 1.50)
        self.inventory.add_item(self.cola, 2)
    
    def test_restock(self):
        """restock should add to existing quantity."""
        self.inventory.restock("A1", 5)
        self.assertEqual(self.inventory.get_quantity("A1"), 7)
    
    def test_restock_returns_true(self):
        """restock should return True on success."""
        result = self.inventory.restock("A1", 5)
        self.assertTrue(result)
    
    def test_restock_nonexistent_returns_false(self):
        """restock should return False for non-existent items."""
        result = self.inventory.restock("Z9", 5)
        self.assertFalse(result)
    
    def test_restock_negative_raises_error(self):
        """restock with negative quantity should raise error."""
        with self.assertRaises(ValueError):
            self.inventory.restock("A1", -1)


class TestInventoryQueries(unittest.TestCase):
    """Test inventory query methods."""
    
    def setUp(self):
        self.inventory = Inventory()
        self.cola = Soda("A1", "Cola", 1.50)
        self.water = Water("C1", "Water", 1.00)
        self.oj = Juice("B1", "OJ", 2.00)
        
        self.inventory.add_item(self.cola, 3)
        self.inventory.add_item(self.water, 0)  # Out of stock
        self.inventory.add_item(self.oj, 2)
    
    def test_get_all_items(self):
        """get_all_items should return all items with details."""
        items = self.inventory.get_all_items()
        self.assertEqual(len(items), 3)
        self.assertIn("A1", items)
        self.assertEqual(items["A1"]["name"], "Cola")
    
    def test_get_available_items(self):
        """get_available_items should only return stocked items."""
        available = self.inventory.get_available_items()
        self.assertEqual(len(available), 2)
        names = [d.name for d in available]
        self.assertIn("Cola", names)
        self.assertIn("OJ", names)
        self.assertNotIn("Water", names)


if __name__ == '__main__':
    unittest.main(verbosity=2)
