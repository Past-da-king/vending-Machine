"""
Unit tests for Payment services.
Tests payment processing and refund functionality.
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from vending_machine.services import CashPaymentService


class TestCashPaymentService(unittest.TestCase):
    """Test the CashPaymentService class."""
    
    def setUp(self):
        self.payment = CashPaymentService()
    
    def test_initial_balance_is_zero(self):
        """Initial balance should be zero."""
        self.assertEqual(self.payment.get_balance(), 0.0)
    
    def test_insert_money(self):
        """Inserting money should increase balance."""
        self.payment.insert_money(1.00)
        self.assertEqual(self.payment.get_balance(), 1.00)
    
    def test_insert_money_multiple(self):
        """Multiple insertions should accumulate."""
        self.payment.insert_money(1.00)
        self.payment.insert_money(0.50)
        self.assertEqual(self.payment.get_balance(), 1.50)
    
    def test_insert_negative_raises_error(self):
        """Inserting negative amount should raise error."""
        with self.assertRaises(ValueError):
            self.payment.insert_money(-1.00)
    
    def test_insert_zero_raises_error(self):
        """Inserting zero should raise error."""
        with self.assertRaises(ValueError):
            self.payment.insert_money(0)
    
    def test_deduct_success(self):
        """deduct should return True and change on success."""
        self.payment.insert_money(2.00)
        success, change = self.payment.deduct(1.50)
        self.assertTrue(success)
        self.assertEqual(change, 0.50)
    
    def test_deduct_exact_amount(self):
        """deduct with exact amount should return 0 change."""
        self.payment.insert_money(1.50)
        success, change = self.payment.deduct(1.50)
        self.assertTrue(success)
        self.assertEqual(change, 0.0)
    
    def test_deduct_insufficient_funds(self):
        """deduct should return False when insufficient funds."""
        self.payment.insert_money(1.00)
        success, change = self.payment.deduct(1.50)
        self.assertFalse(success)
        self.assertEqual(change, 0.0)
    
    def test_deduct_resets_balance(self):
        """deduct should reset balance to zero."""
        self.payment.insert_money(2.00)
        self.payment.deduct(1.50)
        self.assertEqual(self.payment.get_balance(), 0.0)
    
    def test_refund(self):
        """refund should return full balance."""
        self.payment.insert_money(2.50)
        refund = self.payment.refund()
        self.assertEqual(refund, 2.50)
    
    def test_refund_resets_balance(self):
        """refund should reset balance to zero."""
        self.payment.insert_money(2.50)
        self.payment.refund()
        self.assertEqual(self.payment.get_balance(), 0.0)
    
    def test_refund_empty_balance(self):
        """refund with empty balance should return 0."""
        refund = self.payment.refund()
        self.assertEqual(refund, 0.0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
