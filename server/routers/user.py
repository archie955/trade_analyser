from fastapi import APIRouter, status, HTTPException, Depends
from models import schemas, models
from database.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import or_
from utils import utils
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from authentication import auth

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(
        user: schemas.UserCreate,
        db: Session = Depends(get_db)
        ):
    
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This email is already in use"
        )
    
    if db.query(models.User).filter(models.User.username == user.username).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This username is already in use"
        )
    
    hashed_pwd = utils.hash(user.password)

    new_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_pwd
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return schemas.UserOut.model_validate(new_user)

@router.post("/login", status_code=status.HTTP_200_OK, response_model=schemas.Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(or_(
        models.User.email == user_credentials.username,
        models.User.username == user_credentials.username)
        ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid username or password"
        )
    
    if not utils.verify(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid username or password"
        )
    
    user_data = {"sub": str(user.id)}

    access = auth.create_access_token(data=user_data)

    return schemas.Token(access_token = access, token_type = "bearer")

    
@router.put("/", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def update_user(
    updated_payload: schemas.UserUpdate,
    db: Session = Depends(get_db),
    user: models.User = Depends(auth.get_current_user)
):
    password = updated_payload.password
    updated_user = updated_payload.updated_user
    
    if not utils.verify(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )
    
    if (user.email == updated_user.email
        and utils.verify(updated_user.password, user.hashed_password)
        and user.username == updated_user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No updated information provided"
        )
    
    user.email = updated_user.email
    user.username = updated_user.username
    user.hashed_password = utils.hash(updated_user.password)

    db.commit()
    db.refresh(user)

    return schemas.UserOut.model_validate(user)

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    db: Session = Depends(get_db),
    user: models.User = Depends(auth.get_current_user)
):
    
    db.delete(user)
    db.commit()

    return