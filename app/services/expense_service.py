from sqlalchemy.orm import Session
from sqlalchemy import select,extract,func

from uuid import UUID

from app.enums.expense_category import ExpenseCategory
from app.models.expense import Expense
from app.schemas.expense import CreateExpense, UpdateExpense
from app.utils.exceptions import expense_not_found


def create_expense(db:Session,expense_data:CreateExpense)->Expense:
    expense = Expense(
        title=expense_data.title,
        amount=expense_data.amount,
        description=expense_data.description,
        category=expense_data.category,
        expense_date=expense_data.expense_date
    )

    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense

def get_all_expenses(db:Session)->list[Expense]:
    statement = (select(Expense)
                 .where(Expense.is_active.is_(True))
                 .order_by(Expense.expense_date.desc()))

    return list(db.scalars(statement).all())

def get_expense(db: Session, expense_id: UUID) -> Expense:
    expense: Expense | None = db.get(Expense, expense_id)

    if expense is None or not expense.is_active:
        raise expense_not_found()

    return expense

def update_expense(db:Session, expense_id: UUID, expense_data: UpdateExpense)->Expense:
    expense = get_expense(db, expense_id)

    updated_expense = expense_data.model_dump(exclude_unset=True)

    for field,value in updated_expense.items():
        setattr(expense, field, value)

    db.commit()
    db.refresh(expense)
    return expense

def delete_expense(db:Session, expense_id: UUID)->None:
    expense = get_expense(db, expense_id)
    expense.is_active = False
    db.commit()

def get_all_categories(db:Session)->list[ExpenseCategory]:
    statement = (
        select(Expense.category)
                 .where(Expense.is_active.is_(True))
                 .distinct()
                 .order_by(Expense.category)
    )
    return list(db.scalars(statement).all())

def get_expense_by_category(db:Session, category: ExpenseCategory) -> list[Expense]:
    statement = (
        select(Expense)
        .where(Expense.category == category)
        .where(Expense.is_active.is_(True))
        .order_by(Expense.expense_date.desc())
    )
    return list(db.scalars(statement).all())