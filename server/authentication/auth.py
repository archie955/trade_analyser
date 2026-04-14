import jwt
from fastapi.security import OAuth2PasswordBearer
from utils.config import settings
from fastapi import HTTPException, status, Depends, Path
from datetime import datetime, timezone, timedelta
from typing import Dict, Any
from models import schemas, models
from sqlalchemy.orm import Session
from database.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
CREDENTIALS_EXCEPTION = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                      detail="Could not validate credentials",
                                      headers={"WWW-Authenticate": "Bearer"}
                                      )

def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt

def decode_token(token: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload
    except jwt.exceptions.InvalidTokenError:
        raise CREDENTIALS_EXCEPTION
    
def verify_access_token(token:str) -> schemas.TokenData:
    payload = decode_token(token)

    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type"
        )
    
    user_id = payload.get("sub")

    if user_id is None:
        raise CREDENTIALS_EXCEPTION
    
    return schemas.TokenData(id=user_id)

def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
) -> models.User:
    user_id_token = verify_access_token(token=token)

    user = db.query(models.User).filter(models.User.id == int(user_id_token.id)).first()

    if not user:
        raise CREDENTIALS_EXCEPTION
    
    return user

def get_current_league(
        league_id: int = Path(..., description="ID of the league"),
        user: models.User = Depends(get_current_user),
        db: Session = Depends(get_db)
) -> models.League:
    league = db.query(models.League).filter(
        models.League.user_id == user.id,
        models.League.id == league_id).first()
    
    if not league:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"League with id {league_id} not found"
        )
    
    return league