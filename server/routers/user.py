from fastapi import APIRouter, status, HTTPException, Depends
from models import schemas, models
from database.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import or_, select
from utils import utils
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from authentication import auth

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(
        user: schemas.UserCreate,
        db: AsyncSession = Depends(get_db)
        ):
    already_user = (await db.execute(select(models.User).where(
        or_(models.User.email == user.email,
            models.User.username == user.username)
            ))).scalars().all()
    
    if already_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This user already has an account is already in use"
        )
    
    hashed_pwd = utils.hash(user.password)

    new_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_pwd
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return schemas.UserOut.model_validate(new_user)

@router.post("/login", status_code=status.HTTP_200_OK, response_model=schemas.Token)
async def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    user = (await db.execute(select(models.User).where(
        or_(
            models.User.email == user_credentials.username,
            models.User.username == user_credentials.username)
        ))).scalar_one_or_none()
    
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
async def update_user(
    updated_payload: schemas.UserUpdate,
    db: AsyncSession = Depends(get_db),
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

    await db.commit()
    await db.refresh(user)

    return schemas.UserOut.model_validate(user)

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    db: AsyncSession = Depends(get_db),
    user: models.User = Depends(auth.get_current_user)
):
    
    await db.delete(user)
    await db.commit()

    return