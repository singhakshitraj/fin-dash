from enum import Enum

class UserRole(str,Enum):
    VIEWER="viewer"
    ANALYST="analyst"
    ADMIN="admin"

class TransactionType(str,Enum):
    INCOME="income"
    EXPENSE="expense"

class TransactionCategory(str,Enum):
    SALARY="salary"
    FOOD="food"
    RENT="rent"
    SHOPPING="shopping"
    OTHER="other"

