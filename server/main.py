from fastapi import FastAPI, Depends, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from routers import user, league, team, players, trades
from utils.config import settings
from database.database import get_db
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

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
app.include_router(team.router)
app.include_router(players.router)
app.include_router(trades.router)


@app.get("/health")
def health(
    db: Session = Depends(get_db)
):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "healthy"}
    except:
        return {"status": "unhealthy"}
    
@app.exception_handler(Exception)
def global_expression_handler(request: Request, exc: Exception):
    if exc == IntegrityError:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": f"sqlalchemy.exc.IntegrityError for request {request}"}
        )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": f"Internal server error for request {request}"}
    )

@app.get("/")
def root():
    return {"message": "home page"}