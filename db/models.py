from datetime import datetime,timezone
from typing import Optional,List
from sqlalchemy import Boolean,Column,DateTime,Enum as SAEnum,ForeignKey,Integer,Numeric,String,Text
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column,relationship
from .enums import TransactionCategory,TransactionType,UserRole

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__="users"
    
    id: Mapped[int]=mapped_column(Integer,primary_key=True,index=True,autoincrement=True)
    username: Mapped[str]=mapped_column(String(50),unique=True,nullable=False,index=True)
    password: Mapped[str]=mapped_column(String(255),nullable=False)
    role: Mapped[UserRole]=mapped_column(
        SAEnum(UserRole,name="userrole",native_enum=False),
        nullable=False,
        default=UserRole.VIEWER,
        server_default=UserRole.VIEWER.value
    )
    is_active: Mapped[bool]=mapped_column(Boolean,nullable=False,default=True,server_default="true")
    created_at: Mapped[datetime]=mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    records: Mapped[List["FinancialRecord"]]=relationship(
        "FinancialRecord",
        back_populates="owner",
        cascade="all,delete-orphan",
        lazy="select",
    )

class FinancialRecord(Base):
    __tablename__="financial_records"

    id: Mapped[int]=mapped_column(Integer,primary_key=True,index=True,autoincrement=True)
    user_id: Mapped[int]=mapped_column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False,index=True)
    amount: Mapped[float]=mapped_column(Numeric(precision=12,scale=2),nullable=False)
    type: Mapped[TransactionType]=mapped_column(
        SAEnum(TransactionType,name="transactiontype",native_enum=False),
        nullable=False
    )
    category: Mapped[TransactionCategory]=mapped_column(
        SAEnum(TransactionCategory,name="transactioncategory",native_enum=False),
        nullable=False,
        default=TransactionCategory.OTHER
    )
    date: Mapped[datetime]=mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        index=True
    )
    description: Mapped[Optional[str]]=mapped_column(Text,nullable=True)
    created_at: Mapped[datetime]=mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )
    owner: Mapped["User"]=relationship("User",back_populates="records")