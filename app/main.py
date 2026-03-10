from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Guchenung-am Tea Inventory API"}
