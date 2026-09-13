from datetime import date,datetime
from decimal import Decimal
from uuid import UUID

from app.enums.expense_category import ExpenseCategory
from pydantic import BaseModel,ConfigDict, Field, field_validator


class CreateExpense(BaseModel):
    title: str = Field( min_length=1, max_length=25)
    amount:Decimal= Field( gt=0,decimal_places=2,max_digits=10)
    description:str|None = Field(default=None, max_length=100)
    category: ExpenseCategory
    expense_date:date

    @field_validator('title')
    @classmethod
    def strip_text(cls, value : str)->str:
        value = value.strip()
        if not value:
            raise ValueError('Expense title cannot be empty')
        return value


class UpdateExpense(BaseModel):
    title: str|None = Field(default=None, min_length=1, max_length=25)
    amount:Decimal|None= Field(default=None, gt=0,decimal_places=2,max_digits=10)
    description:str|None = Field(default=None, max_length=100)
    category: ExpenseCategory | None = None
    expense_date:date|None = None

    @field_validator('title')
    @classmethod
    def strip_text(cls, value : str|None)->str|None:
        if value is None:
            return value
        value = value.strip()
        if not value:
            raise ValueError('Expense title cannot be empty')
        return value

class ExpenseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id : UUID
    title : str
    amount : Decimal
    description: str | None
    category : ExpenseCategory
    expense_date : date
    created_at : datetime
    updated_at : datetime

class CategoryResponse(BaseModel):
    categories: list[ExpenseCategory]