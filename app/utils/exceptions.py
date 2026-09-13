from fastapi import HTTPException,status

def expense_not_found()->HTTPException:
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Expense not found")