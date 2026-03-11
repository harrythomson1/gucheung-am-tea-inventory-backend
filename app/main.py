from fastapi import FastAPI

from app.routes import tea

app = FastAPI()

app.include_router(tea.router)


@app.get("/")
def root():
    return {"message": "Guchenung-am Tea Inventory API"}
