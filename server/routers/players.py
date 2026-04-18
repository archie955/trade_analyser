from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from models import models, schemas
from database.database import get_db
from authentication.auth import get_current_team

router = APIRouter(prefix="/players", tags=["Players"])

def fetch_player(
        id: int,
        db: Session = Depends(get_db)
):
    player_db = db.query(models.Player).filter(
        models.Player.id == id
    ).first()

    if not player_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Player not found"
        )
    
    return schemas.PlayerOut.model_validate(player_db)


@router.post("/{team_id}", status_code=status.HTTP_201_CREATED, response_model=schemas.PlayerOut)
def add_player(
    id: int,
    db: Session = Depends(get_db),
    team: models.Team = Depends(get_current_team)
):
    player = fetch_player(id)

    already_added = db.query(models.TeamPlayer).filter(
        models.TeamPlayer.team_id == team.id,
        models.TeamPlayer.player_id == player.id
    ).first()

    if already_added:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Players already added"
        )
    
    team.players.append(player)

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
def remove_player(
    id: int,
    db: Session = Depends(get_db),
    team: models.Team = Depends(get_current_team)
):
    player_to_delete = db.query(models.TeamPlayer).filter(
        models.TeamPlayer.player_id == id,
        models.TeamPlayer.team_id == team.id
    ).first()

    if not player_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player with id {id} not found to delete"
        )
    
    db.delete(player_to_delete)
    db.commit()

    return
    