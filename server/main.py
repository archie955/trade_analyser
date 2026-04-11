from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from routers import user, league
from utils.config import settings
from database.database import get_db
from sqlalchemy import text
from sqlalchemy.orm import Session

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(user.router)
app.include_router(league.router)


@app.get("/health")
def health(
    db: Session = Depends(get_db)
):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "healthy"}
    except:
        return {"status": "unhealthy"}

@app.get("/")
def root():
    return {"message": "home page"}