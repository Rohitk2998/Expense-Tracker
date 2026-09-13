from enum import Enum

class ExpenseCategory(str,Enum):
    FOOD = "food"
    TRAVEL = "travel"
    SHOPPING = "shopping"
    BILLS = "bills"
    ENTERTAINMENT = "entertainment"
    HEALTH = "health"
    EDUCATION = "education"
    OTHER = "other"