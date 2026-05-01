from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import models, schemas
from database.database import get_db
from authentication.auth import get_current_team

router = APIRouter(prefix="/players", tags=["Players"])

async def fetch_player(
        id: int,
        db: AsyncSession = Depends(get_db)
):
    player_db = (await db.execute(select(models.Player).where(
        models.Player.id == id
    ))).scalar_one_or_none()

    if not player_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Player not found"
        )
    
    return schemas.PlayerOut.model_validate(player_db)


@router.post("/{team_id}", status_code=status.HTTP_201_CREATED, response_model=schemas.PlayerOut)
async def add_player(
    id: int,
    db: AsyncSession = Depends(get_db),
    team: models.Team = Depends(get_current_team)
):
    player = await fetch_player(id)

    already_added = (await db.execute(select(models.TeamPlayer).where(
        models.TeamPlayer.team_id == team.id,
        models.TeamPlayer.player_id == player.id
    ))).scalar_one_or_none()

    if already_added:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Players already added"
        )
    
    team.players.append(player)

    await db.commit()

    return player
    
@router.get("/{team_id}", status_code=status.HTTP_200_OK, response_model=schemas.TeamPlayers)
def get_team_players(
    team: models.Team = Depends(get_current_team)
):
    players = team.players

    if players is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This team has no initialised players"
        )
    
    players_list = [schemas.PlayerOut.model_validate(player) for player in players]

    return schemas.TeamPlayers(players=players_list)

@router.delete("/{team_id}/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_player(
    id: int,
    db: AsyncSession = Depends(get_db),
    team: models.Team = Depends(get_current_team)
):
    player_to_delete = (await db.execute(select(models.TeamPlayer).where(
        models.TeamPlayer.player_id == id,
        models.TeamPlayer.team_id == team.id
    ))).scalar_one_or_none()

    if not player_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player with id {id} not found to delete"
        )
    
    await db.delete(player_to_delete)
    await db.commit()

    return
    