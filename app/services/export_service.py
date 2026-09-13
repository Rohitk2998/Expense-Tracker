import csv
import io
import json

from app.models.expense import Expense


def expense_to_csv(expenses:list[Expense])->io.BytesIO:
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
            "id",
            "title",
            "amount",
            "category",
            "description",
            "expense_date",
            "created_at",
            "updated_at",
        ])

    for expense in expenses:
        writer.writerow([
            str(expense.id),
            expense.title,
            str(expense.amount),
            expense.category.value.capitalize(),
            expense.description or "",
            expense.expense_date.isoformat(),
            expense.created_at.isoformat(),
            expense.updated_at.isoformat(),
        ])

    file = io.BytesIO(output.getvalue().encode('utf-8'))

    file.seek(0)

    return file


def expense_to_json(expenses:list[Expense])->io.BytesIO:
    data = []
    for expense in expenses:
        data.append({
            "id": str(expense.id),
            "title": expense.title,
            "amount": str(expense.amount),
            "category": expense.category.value.capitalize(),
            "description": expense.description or "",
            "expense_date": expense.expense_date,
            "created_at": expense.created_at,
            "updated_at": expense.updated_at,
        })

    file = io.BytesIO(json.dumps(data,default=str).encode('utf-8'))

    file.seek(0)

    return file