from decimal import Decimal

from sqlalchemy.orm import Session
from sqlalchemy import func, select, extract

from app.models.expense import Expense


def get_total_expense(db:Session)->Decimal:
    statement = select(
        func.coalesce(
            func.sum(Expense.amount),0
        )
    ).where(
        Expense.is_active.is_(True)
    )

    return db.scalar(statement)

def get_monthly_expense(db:Session):
    statement = (select(
        extract("year", Expense.expense_date).label("year"),
        extract("month", Expense.expense_date).label("month"),
        func.coalesce(
            func.sum(Expense.amount),0
        ).label(
            "total_spending"
        )
    ).where(
        Expense.is_active.is_(True)
    ).group_by(
        extract("year", Expense.expense_date),
        extract("month", Expense.expense_date),
    ).order_by(
        extract("year", Expense.expense_date),
        extract("month", Expense.expense_date),
    ))

    return db.execute(statement).all()

def get_category_expense(db:Session):
    statement = select(
        Expense.category,
        func.coalesce(
            func.sum(Expense.amount),0
        ).label(
            "total_spending"
        )
    ).where(
        Expense.is_active.is_(True)
    ).group_by(
        Expense.category,
    ).order_by(
        func.coalesce(
            func.sum(Expense.amount),0
        ).desc()
    )

    return db.execute(statement).all()

def get_highest_expense_summary(db:Session)->Expense|None:
    statement = (
        select(Expense)
            .where(
                Expense.is_active.is_(True)
            ).order_by(
                Expense.amount.desc()
            ).limit(1)
    )

    return db.scalars(statement).first()
