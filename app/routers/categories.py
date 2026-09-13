from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.enums.expense_category import ExpenseCategory
from app.schemas.expense import  ExpenseResponse
from app.services.expense_service import get_all_categories, get_expense_by_category

router = APIRouter(prefix="/api", tags=["Categories"])

@router.get("/categories", response_model=list[ExpenseCategory])
def list_categories(db:Session=Depends(get_db)):
    return get_all_categories(db)

@router.get("/expenses/category/{category}", response_model=list[ExpenseResponse])
def list_expense_by_category(category:ExpenseCategory, db:Session=Depends(get_db)):
    return get_expense_by_category(db, category)
