from fastapi import FastAPI

from auth.auth_router import router as auth_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth")

@app.get("/")
def get_home():
    return{"message": "hii"}

