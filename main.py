from fastapi import FastAPI

from auth.auth_router import router as auth_router
from cv.cv_router import router as cv_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(cv_router)

@app.get("/")
def get_home():
    return{"message": "hii"}

