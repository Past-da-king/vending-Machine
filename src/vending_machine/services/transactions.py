"""
Transaction management service.
Tracks all purchases and provides statistics.
"""
from datetime import datetime
from typing import List, Dict, Optional
from enum import Enum


class TransactionStatus(Enum):
    """Status of a transaction."""
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class Transaction:
    """
    Represents a single transaction.
    
    Immutable record of a purchase attempt with all relevant details.
    """
    
    _counter = 0
    
    def __init__(
        self,
        item_code: str,
        item_name: str,
        item_price: float,
        amount_paid: float,
        change_given: float,
        status: TransactionStatus
    ):
        Transaction._counter += 1
        self._id = f"TXN-{Transaction._counter:04d}"
        self._timestamp = datetime.now()
        self._item_code = item_code
        self._item_name = item_name
        self._item_price = item_price
        self._amount_paid = amount_paid
        self._change_given = change_given
        self._status = status
    
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def timestamp(self) -> datetime:
        return self._timestamp
    
    @property
    def item_code(self) -> str:
        return self._item_code
    
    @property
    def item_name(self) -> str:
        return self._item_name
    
    @property
    def item_price(self) -> float:
        return self._item_price
    
    @property
    def amount_paid(self) -> float:
        return self._amount_paid
    
    @property
    def change_given(self) -> float:
        return self._change_given
    
    @property
    def status(self) -> TransactionStatus:
        return self._status
    
    def to_dict(self) -> Dict:
        """Convert transaction to dictionary representation."""
        return {
            'id': self._id,
            'timestamp': self._timestamp.isoformat(),
            'item_code': self._item_code,
            'item_name': self._item_name,
            'item_price': self._item_price,
            'amount_paid': self._amount_paid,
            'change_given': self._change_given,
            'status': self._status.value
        }


class TransactionService:
    """
    Manages transaction history and statistics.
    
    Provides methods for recording transactions and generating reports.
    """
    
    def __init__(self):
        self._transactions: List[Transaction] = []
    
    def record(self, transaction: Transaction) -> None:
        """Record a new transaction."""
        self._transactions.append(transaction)
    
    def create_success(
        self,
        item_code: str,
        item_name: str,
        item_price: float,
        amount_paid: float,
        change_given: float
    ) -> Transaction:
        """Create and record a successful transaction."""
        txn = Transaction(
            item_code, item_name, item_price,
            amount_paid, change_given, TransactionStatus.SUCCESS
        )
        self.record(txn)
        return txn
    
    def create_failed(
        self,
        item_code: str,
        item_name: str,
        item_price: float,
        amount_paid: float,
        reason: str = ""
    ) -> Transaction:
        """Create and record a failed transaction."""
        txn = Transaction(
            item_code, item_name, item_price,
            amount_paid, 0.0, TransactionStatus.FAILED
        )
        self.record(txn)
        return txn
    
    def get_all(self) -> List[Dict]:
        """Get all transactions as dictionaries."""
        return [t.to_dict() for t in self._transactions]
    
    def get_successful(self) -> List[Transaction]:
        """Get all successful transactions."""
        return [t for t in self._transactions if t.status == TransactionStatus.SUCCESS]
    
    def get_statistics(self) -> Dict:
        """
        Get transaction statistics.
        
        Returns:
            Dictionary with total, successful, failed counts and revenue
        """
        successful = self.get_successful()
        return {
            'total_transactions': len(self._transactions),
            'successful': len(successful),
            'failed': len(self._transactions) - len(successful),
            'total_revenue': sum(t.item_price for t in successful),
            'success_rate': (
                len(successful) / len(self._transactions) * 100
                if self._transactions else 0
            )
        }
