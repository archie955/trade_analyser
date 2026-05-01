from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import models, schemas
from database.database import get_db
from authentication.auth import get_current_user

router = APIRouter(prefix="/leagues", tags=["Leagues"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.LeagueOut)
async def create_league(
    league: schemas.LeagueCreate,
    db: AsyncSession = Depends(get_db),
    user: models.User = Depends(get_current_user)
):
    results = await db.execute(select(models.League).where(
        models.League.name == league.name,
        models.League.user_id == user.id
    ))
    
    already_exists = results.scalar_one_or_none()

    if already_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"League already exists"
        )

    db_league = models.League(user_id=user.id, **league.model_dump())

    db.add(db_league)
    await db.commit()
    await db.refresh(db_league)

    return schemas.LeagueOut.model_validate(db_league)



@router.get("/", status_code=status.HTTP_200_OK, response_model=schemas.Leagues)
async def get_leagues(
    db: AsyncSession = Depends(get_db),
    user: models.User = Depends(get_current_user)
):
    results = await db.execute(select(models.League).where(
        models.League.user_id == user.id
    ))
    leagues = results.scalars().all()

    league_list = [schemas.LeagueOut.model_validate(league) for league in leagues]

    return schemas.Leagues(leagues=league_list)



@router.put("/", status_code=status.HTTP_200_OK, response_model=schemas.LeagueOut)
async def update_league_info(
    updated_league: schemas.LeagueUpdate,
    db: AsyncSession = Depends(get_db),
    user: models.User = Depends(get_current_user)
):
    results = await db.execute(select(models.League).where(
        models.League.id == updated_league.id,
        models.League.user_id == user.id
    ))
    league_to_update = results.scalar_one_or_none()

    if not league_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="League not found to update"
            )
    
    league_to_update.name = updated_league.name

    await db.commit()
    await db.refresh(league_to_update)
    
    return schemas.LeagueOut.model_validate(league_to_update)



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_league(
    id: int,
    db: AsyncSession = Depends(get_db),
    user: models.User = Depends(get_current_user)
):
    results = await db.execute(select(models.League).where(
        models.League.user_id == user.id,
        models.League.id == id
    ))
    league_to_delete = results.scalar_one_or_none()

    if not league_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"League with id {id} not found to delete"
            )
    
    await db.delete(league_to_delete)
    await db.commit()

    return

