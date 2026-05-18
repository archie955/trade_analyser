from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import models, schemas
from database.database import get_db
from authentication.auth import get_current_team

router = APIRouter(
    prefix="/leagues/{league_id}/teams/{team_id}/players", tags=["Team Players"]
)


@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=schemas.TeamPlayerOut
)
async def add_player(
    player_in: schemas.TeamPlayerIn,
    db: AsyncSession = Depends(get_db),
    team: models.Team = Depends(get_current_team),
):
    player = (
        await db.execute(select(models.Player).where(models.Player.id == player_in.id))
    ).scalar_one_or_none()

    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Player not found"
        )

    already_added = (
        await db.execute(
            select(models.TeamPlayer).where(
                models.TeamPlayer.league_id == team.league_id,
                models.TeamPlayer.player_id == player.id,
            )
        )
    ).scalar_one_or_none()

    if already_added:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Players already added"
        )
    team_player = models.TeamPlayer(
        league_id=team.league_id, team_id=team.id, player_id=player.id
    )
    db.add(team_player)

    await db.commit()

    return schemas.TeamPlayerOut.model_validate(player)


@router.get("", status_code=status.HTTP_200_OK, response_model=schemas.TeamPlayers)
def get_team_players(team: models.Team = Depends(get_current_team)):
    players = team.players

    if not players:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No players in this team"
        )

    players_list = [schemas.TeamPlayerOut.model_validate(player) for player in players]

    return schemas.TeamPlayers(players=players_list)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_player(
    id: int,
    db: AsyncSession = Depends(get_db),
    team: models.Team = Depends(get_current_team),
):
    player_to_delete = (
        await db.execute(
            select(models.TeamPlayer).where(
                models.TeamPlayer.player_id == id, models.TeamPlayer.team_id == team.id
            )
        )
    ).scalar_one_or_none()

    if not player_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player with id {id} not found to delete",
        )

    await db.delete(player_to_delete)
    await db.commit()

    return
