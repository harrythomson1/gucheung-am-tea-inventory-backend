from fastapi import FastAPI

from app.routes import dashboard, tea, transaction

app = FastAPI()

app.include_router(tea.router)
app.include_router(transaction.router)
app.include_router(dashboard.router)


@app.get("/")
def root():
    return {"message": "Guchenung-am Tea Inventory API"}
