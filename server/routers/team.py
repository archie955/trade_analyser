from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import models, schemas
from database.database import get_db
from authentication.auth import get_current_league

router = APIRouter(prefix="/leagues/{league_id}/teams", tags=["Teams"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.TeamOut)
async def create_team(
    team: schemas.TeamCreate,
    db: AsyncSession = Depends(get_db),
    league: models.League = Depends(get_current_league)
):
    already_exists = (await db.execute(select(models.Team).where(
        models.Team.name == team.name,
        models.Team.league_id == league.id 
    ))).scalar_one_or_none()
    
    if already_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Team already exists"
        )
    
    db_team = models.Team(user_id=league.user_id, league_id=league.id, **team.model_dump())

    db.add(db_team)
    await db.commit()
    await db.refresh(db_team)

    return schemas.TeamOut.model_validate(db_team)


@router.get("/", status_code=status.HTTP_200_OK, response_model=schemas.Teams)
async def get_league_teams(
    db: AsyncSession = Depends(get_db),
    league: models.League = Depends(get_current_league)
):
    teams = (await db.execute(select(models.Team).where(
        models.Team.league_id == league.id
    ))).scalars().all()

    team_list = [schemas.TeamOut.model_validate(team) for team in teams]

    return schemas.Teams(teams=team_list)

@router.put("/", status_code=status.HTTP_200_OK, response_model=schemas.TeamOut)
async def update_team_info(
    updated_team: schemas.TeamUpdate,
    db: AsyncSession = Depends(get_db),
    league: models.League = Depends(get_current_league)
):
    team_to_update = (await db.execute(select(models.Team).where(
        models.Team.league_id == league.id,
        models.Team.id == updated_team.id
    ))).scalar_one_or_none()

    if not team_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found to update"
        )
    
    team_to_update.name = updated_team.name

    await db.commit()
    await db.refresh(team_to_update)

    return schemas.TeamOut.model_validate(team_to_update)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_team(
    id: int,
    db: AsyncSession = Depends(get_db),
    league: models.User = Depends(get_current_league)
):
    team_to_delete = (await db.execute(select(models.Team).where(
        models.Team.league_id == league.id,
        models.Team.id == id
    ))).scalar_one_or_none()

    if not team_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with id {id} not found to delete"
        )
    
    await db.delete(team_to_delete)
    await db.commit()

    return



