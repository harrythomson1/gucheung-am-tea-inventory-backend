from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import dashboard, tea, transaction

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://gucheung-am-inventory-frontend-506nj52ma.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tea.router)
app.include_router(transaction.router)
app.include_router(dashboard.router)


@app.get("/health")
def health():
    return {"status": "ok"}
