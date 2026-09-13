
from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException

from app.database import get_db
from app.services.email_service import send_email
from app.services.expense_service import get_all_expenses
from app.services.summary_service import get_total_expense

router = APIRouter(
    prefix="/api/expenses/report/email/{email_id}",
    tags=["reports"]
)

@router.post("/")
def send_email_report( email_id: str,db:Session=Depends(get_db)):
    expenses = get_all_expenses(db)

    total = get_total_expense(db)

    report_lines = [
        "Expense Report",
        '='*30,
        "",
        f"Total spending: {total}",
        f"Number of expenses: {len(expenses)}",
        "",
        "Last 30 expenses",
        "-"*30,
    ]

    for expense in expenses:
            report_lines.append(
                f"{expense.expense_date} | "
                f"{expense.category.value.capitalize} | "
                f"{expense.title} | "
                f"{expense.amount}"
            )

    report = "\n".join(report_lines)

    try:
        send_email(report,email_id)
    except Exception as e:
        raise HTTPException(status_code=500,detail="Failed to send email")


    return {
        "message"   : "Expense Report Sent"
    }