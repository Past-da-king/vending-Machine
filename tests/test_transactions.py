"""
Unit tests for Transaction services.
Tests transaction recording and statistics.
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from vending_machine.services import TransactionService, TransactionStatus


class TestTransactionService(unittest.TestCase):
    """Test the TransactionService class."""
    
    def setUp(self):
        self.service = TransactionService()
    
    def test_initial_empty(self):
        """Service should start with no transactions."""
        self.assertEqual(len(self.service.get_all()), 0)
    
    def test_create_success_transaction(self):
        """create_success should create and record a transaction."""
        txn = self.service.create_success(
            "A1", "Cola", 1.50, 2.00, 0.50
        )
        self.assertEqual(txn.status, TransactionStatus.SUCCESS)
        self.assertEqual(txn.item_name, "Cola")
        self.assertEqual(txn.item_price, 1.50)
        self.assertEqual(txn.change_given, 0.50)
    
    def test_create_failed_transaction(self):
        """create_failed should create a failed transaction."""
        txn = self.service.create_failed(
            "A1", "Cola", 1.50, 1.00, "Insufficient funds"
        )
        self.assertEqual(txn.status, TransactionStatus.FAILED)
    
    def test_transaction_has_id(self):
        """Transactions should have unique IDs."""
        txn1 = self.service.create_success("A1", "Cola", 1.50, 2.00, 0.50)
        txn2 = self.service.create_success("A2", "Pepsi", 1.50, 2.00, 0.50)
        self.assertNotEqual(txn1.id, txn2.id)
    
    def test_transaction_has_timestamp(self):
        """Transactions should have timestamps."""
        txn = self.service.create_success("A1", "Cola", 1.50, 2.00, 0.50)
        self.assertIsNotNone(txn.timestamp)
    
    def test_get_all_returns_list(self):
        """get_all should return list of dictionaries."""
        self.service.create_success("A1", "Cola", 1.50, 2.00, 0.50)
        result = self.service.get_all()
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], dict)
    
    def test_get_successful(self):
        """get_successful should only return successful transactions."""
        self.service.create_success("A1", "Cola", 1.50, 2.00, 0.50)
        self.service.create_failed("A2", "Pepsi", 1.50, 1.00, "")
        self.service.create_success("A3", "Sprite", 1.25, 2.00, 0.75)
        
        successful = self.service.get_successful()
        self.assertEqual(len(successful), 2)


class TestTransactionStatistics(unittest.TestCase):
    """Test transaction statistics."""
    
    def setUp(self):
        self.service = TransactionService()
        # Create mix of transactions
        self.service.create_success("A1", "Cola", 1.50, 2.00, 0.50)
        self.service.create_success("A2", "Pepsi", 1.50, 2.00, 0.50)
        self.service.create_failed("A3", "Sprite", 1.25, 1.00, "")
        self.service.create_success("B1", "OJ", 2.00, 3.00, 1.00)
    
    def test_total_transactions(self):
        """Statistics should show correct total."""
        stats = self.service.get_statistics()
        self.assertEqual(stats['total_transactions'], 4)
    
    def test_successful_count(self):
        """Statistics should show correct successful count."""
        stats = self.service.get_statistics()
        self.assertEqual(stats['successful'], 3)
    
    def test_failed_count(self):
        """Statistics should show correct failed count."""
        stats = self.service.get_statistics()
        self.assertEqual(stats['failed'], 1)
    
    def test_total_revenue(self):
        """Statistics should calculate correct revenue."""
        stats = self.service.get_statistics()
        self.assertEqual(stats['total_revenue'], 5.00)  # 1.50 + 1.50 + 2.00
    
    def test_success_rate(self):
        """Statistics should calculate correct success rate."""
        stats = self.service.get_statistics()
        self.assertEqual(stats['success_rate'], 75.0)


class TestEmptyStatistics(unittest.TestCase):
    """Test statistics with no transactions."""
    
    def test_empty_statistics(self):
        """Empty service should return zeros."""
        service = TransactionService()
        stats = service.get_statistics()
        
        self.assertEqual(stats['total_transactions'], 0)
        self.assertEqual(stats['successful'], 0)
        self.assertEqual(stats['failed'], 0)
        self.assertEqual(stats['total_revenue'], 0)
        self.assertEqual(stats['success_rate'], 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
