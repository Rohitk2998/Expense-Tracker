from app.database import Base
from app.enums.expense_category import ExpenseCategory

from uuid import UUID,uuid4
from datetime import date,datetime
from decimal import Decimal

from sqlalchemy import Date,DateTime,Numeric,String,Boolean,func, Enum as SQLEnum
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy.dialects.postgresql import UUID as  PG_UUID

class Expense(Base):
    __tablename__ = 'expenses'

    id : Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True),primary_key=True,default=uuid4)

    title : Mapped[str] = mapped_column(String(25),nullable=False)

    amount : Mapped[Decimal] = mapped_column(Numeric(12,2),nullable=False)

    description : Mapped[str | None] = mapped_column(String(100),nullable=True)

    category : Mapped[ExpenseCategory] = mapped_column(SQLEnum(ExpenseCategory),nullable=False,index=True)

    expense_date : Mapped[date] = mapped_column(Date,nullable=False,index=True)

    is_active : Mapped[bool] = mapped_column(Boolean,nullable=False,default=True)

    created_at : Mapped[datetime] = mapped_column(DateTime,server_default=func.now(),nullable=False)

    updated_at : Mapped[datetime] = mapped_column(DateTime,server_default=func.now(),onupdate=func.now(),nullable=False)


