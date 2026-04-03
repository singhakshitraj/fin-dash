from pydantic import BaseModel
from db.enums import TransactionType,TransactionCategory
from typing import Optional
from datetime import datetime

class FinancialRecordCreateValidation(BaseModel):
    amount:float
    type:TransactionType
    category:TransactionCategory
    description: str|None=None
    

class FinancialRecordUpdateValidation(BaseModel):
    amount: Optional[float] = None
    type: Optional[TransactionType] = None
    category: Optional[TransactionCategory] = None
    date: Optional[datetime] = None
    description: Optional[str] = None