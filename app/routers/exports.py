from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import StreamingResponse

from app.database import get_db
from app.services.expense_service import get_all_expenses
from app.services.export_service import expense_to_csv, expense_to_json

router = APIRouter(
    prefix="/api/expenses/export",
    tags=["exports"],
)

@router.get("/csv")
def export_csv(db:Session=Depends(get_db)):
    expenses = get_all_expenses(db=db)

    file = expense_to_csv(expenses)

    return StreamingResponse(
        file,
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=expenses.csv",
        }
    )

@router.get("/json")
def export_json(db:Session=Depends(get_db)):
    expenses = get_all_expenses(db=db)

    file = expense_to_json(expenses)

    return StreamingResponse(
        file,
        media_type="application/json",
        headers={
            "Content-Disposition": "attachment; filename=expenses.json",
        }
    )