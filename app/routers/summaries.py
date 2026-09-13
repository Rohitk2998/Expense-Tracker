from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.engine import row
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.expense import ExpenseResponse
from app.schemas.summary import TotalSummary, MonthlySummary, CategorySummary
from app.services.summary_service import get_total_expense, get_monthly_expense, get_highest_expense_summary, \
    get_category_expense
from app.utils.exceptions import expense_not_found

router= APIRouter(
    prefix="/api/expenses/summary",
    tags=["expenses"]
)

@router.get("/total", response_model=TotalSummary)
def get_total_summary(db:Session=Depends(get_db))->TotalSummary:
    return TotalSummary(total_spending =get_total_expense(db))

@router.get("/monthly", response_model=list[MonthlySummary])
def get_monthly_summary(db:Session=Depends(get_db))->list[MonthlySummary]:
    result = get_monthly_expense(db)
    return [
        MonthlySummary(
            year=int(row.year),
            month=int(row.month),
            total_spending=row.total_spending
        )
        for row in result
    ]

@router.get("/highest", response_model=ExpenseResponse)
def get_highest_expense(db:Session=Depends(get_db))->ExpenseResponse:
    expense = get_highest_expense_summary(db)
    if expense is None:
        raise expense_not_found()
    return ExpenseResponse.model_validate(expense)

@router.get("/category", response_model=list[CategorySummary])
def get_category_summary(db:Session=Depends(get_db))->list[CategorySummary]:
    result = get_category_expense(db)
    return [
        CategorySummary(
            category=row.category,
            total_spending=row.total_spending
        )
        for row in result
    ]