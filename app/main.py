from fastapi import FastAPI

from app.database import Base, engine
from app.routers.expenses import router as expense_router
from app.routers.exports import router as export_router
from app.routers.categories import router as category_router
from app.routers.summaries import router as summary_router
from app.routers.reports import router as report_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Expense Tracker API",
    description="Expense Tracker using FastAPI and PostgreSQL",
    version="1.0.0",
)

app.include_router(expense_router)
app.include_router(export_router)
app.include_router(category_router)
app.include_router(summary_router)
app.include_router(report_router)

