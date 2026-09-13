from pydantic import BaseModel
from decimal import Decimal
from app.enums.expense_category import ExpenseCategory

class TotalSummary(BaseModel):
    total_spending : Decimal

class MonthlySummary(BaseModel):
    year: int
    month: int
    total_spending : Decimal

class CategorySummary(BaseModel):
    category: ExpenseCategory
    total_spending : Decimal