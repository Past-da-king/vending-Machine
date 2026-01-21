"""
Unit tests for the Drink models.
Tests the inheritance hierarchy and polymorphic behavior.
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from vending_machine.models import Drink, Soda, Juice, Water


class TestDrinkBase(unittest.TestCase):
    """Test the abstract Drink base class."""
    
    def test_cannot_instantiate_abstract_drink(self):
        """Drink is abstract and cannot be instantiated directly."""
        with self.assertRaises(TypeError):
            Drink("X1", "Generic Drink", 1.00)
    
    def test_negative_price_raises_error(self):
        """Creating a drink with negative price should raise ValueError."""
        with self.assertRaises(ValueError):
            Soda("X1", "Bad Drink", -1.00)


class TestSoda(unittest.TestCase):
    """Test the Soda class."""
    
    def setUp(self):
        self.regular_soda = Soda("A1", "Cola", 1.50)
        self.diet_soda = Soda("A2", "Diet Cola", 1.50, is_diet=True)
    
    def test_soda_properties(self):
        """Soda should have correct properties."""
        self.assertEqual(self.regular_soda.code, "A1")
        self.assertEqual(self.regular_soda.name, "Cola")
        self.assertEqual(self.regular_soda.price, 1.50)
    
    def test_soda_category(self):
        """Soda should return correct category."""
        self.assertEqual(self.regular_soda.get_category(), "Soda")
    
    def test_soda_description(self):
        """Soda should return appropriate description."""
        self.assertIn("Carbonated", self.regular_soda.get_description())
    
    def test_diet_soda_description(self):
        """Diet soda should include 'Diet' in description."""
        self.assertIn("Diet", self.diet_soda.get_description())
    
    def test_soda_is_diet_property(self):
        """is_diet property should work correctly."""
        self.assertFalse(self.regular_soda.is_diet)
        self.assertTrue(self.diet_soda.is_diet)
    
    def test_soda_str_representation(self):
        """String representation should be formatted correctly."""
        self.assertEqual(str(self.regular_soda), "Cola ($1.50)")


class TestJuice(unittest.TestCase):
    """Test the Juice class."""
    
    def setUp(self):
        self.juice = Juice("B1", "Orange Juice", 2.00, fruit_type="Orange")
    
    def test_juice_properties(self):
        """Juice should have correct properties."""
        self.assertEqual(self.juice.code, "B1")
        self.assertEqual(self.juice.name, "Orange Juice")
        self.assertEqual(self.juice.price, 2.00)
        self.assertEqual(self.juice.fruit_type, "Orange")
    
    def test_juice_category(self):
        """Juice should return correct category."""
        self.assertEqual(self.juice.get_category(), "Juice")
    
    def test_juice_description(self):
        """Juice should include fruit type in description."""
        desc = self.juice.get_description()
        self.assertIn("Orange", desc)
        self.assertIn("juice", desc.lower())


class TestWater(unittest.TestCase):
    """Test the Water class."""
    
    def setUp(self):
        self.still_water = Water("C1", "Spring Water", 1.00)
        self.sparkling = Water("C2", "Sparkling Water", 1.25, is_sparkling=True)
    
    def test_water_properties(self):
        """Water should have correct properties."""
        self.assertEqual(self.still_water.code, "C1")
        self.assertEqual(self.still_water.name, "Spring Water")
        self.assertEqual(self.still_water.price, 1.00)
    
    def test_water_category(self):
        """Water should return correct category."""
        self.assertEqual(self.still_water.get_category(), "Water")
    
    def test_still_water_description(self):
        """Still water should have 'Still' in description."""
        self.assertIn("Still", self.still_water.get_description())
    
    def test_sparkling_water_description(self):
        """Sparkling water should have 'Sparkling' in description."""
        self.assertIn("Sparkling", self.sparkling.get_description())
    
    def test_is_sparkling_property(self):
        """is_sparkling property should work correctly."""
        self.assertFalse(self.still_water.is_sparkling)
        self.assertTrue(self.sparkling.is_sparkling)


class TestPolymorphism(unittest.TestCase):
    """Test polymorphic behavior across drink types."""
    
    def test_all_drinks_have_category(self):
        """All drink types should implement get_category."""
        drinks = [
            Soda("A1", "Cola", 1.50),
            Juice("B1", "OJ", 2.00),
            Water("C1", "Water", 1.00)
        ]
        categories = [d.get_category() for d in drinks]
        self.assertEqual(categories, ["Soda", "Juice", "Water"])
    
    def test_all_drinks_have_description(self):
        """All drink types should implement get_description."""
        drinks = [
            Soda("A1", "Cola", 1.50),
            Juice("B1", "OJ", 2.00),
            Water("C1", "Water", 1.00)
        ]
        for drink in drinks:
            desc = drink.get_description()
            self.assertIsInstance(desc, str)
            self.assertTrue(len(desc) > 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
