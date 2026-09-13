from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import Response

from app.database import get_db
from uuid import UUID
from app.enums.expense_category import ExpenseCategory
from app.schemas.expense import ExpenseResponse, CreateExpense, UpdateExpense
from app.services.expense_service import create_expense, get_expense, get_all_expenses, update_expense, delete_expense

router = APIRouter(
    prefix="/api/expenses",
    tags=["expenses"]
)

#create
@router.post("/",response_model=ExpenseResponse,status_code=status.HTTP_201_CREATED)
def add_expense(expense_data:CreateExpense,db:Session=Depends(get_db)):
    return create_expense(db,expense_data)

#get by ID
@router.get("/{expense_id}", response_model=ExpenseResponse,status_code=status.HTTP_200_OK)
def get_expense_by_id(expense_id:UUID,db:Session=Depends(get_db)):
    return get_expense(db,expense_id)

#get all expenses
@router.get("/",response_model=list[ExpenseResponse],status_code=status.HTTP_200_OK)
def get_expenses(db:Session=Depends(get_db)):
    return get_all_expenses(db)

#update
@router.put("/{expense_id}", response_model=ExpenseResponse,status_code=status.HTTP_200_OK)
def update_expense_by_id(expense_id:UUID,expense_data:UpdateExpense,db:Session=Depends(get_db)):
    return update_expense(db,expense_id,expense_data)

#delete
@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense_by_id(expense_id:UUID,db:Session=Depends(get_db)):
    delete_expense(db,expense_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


