from fastapi import FastAPI

from app.routes import tea, transaction

app = FastAPI()

app.include_router(tea.router)
app.include_router(transaction.router)


@app.get("/")
def root():
    return {"message": "Guchenung-am Tea Inventory API"}
