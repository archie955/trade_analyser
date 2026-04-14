from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from models import models, schemas
from database.database import get_db
from authentication.auth import get_current_league

router = APIRouter(prefix="/teams", tags=["Teams"])

# fill later