from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from models import models, schemas
from database.database import get_db
from authentication.auth import get_current_league

router = APIRouter(prefix="/teams", tags=["Teams"])

@router.post("/{league_id}", status_code=status.HTTP_201_CREATED, response_model=schemas.TeamOut)
def create_team(
    team: schemas.TeamCreate,
    db: Session = Depends(get_db),
    league: models.League = Depends(get_current_league)
):
    already_exists = db.query(models.Team).filter(
        models.Team.name == team.name,
        models.Team.league_id == league.id).first()
    
    if already_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Team already exists"
        )
    
    db_team = models.Team(user_id=league.user_id, league_id=league.id, **team.model_dump())

    db.add(db_team)
    db.commit()
    db.refresh(db_team)

    return schemas.TeamOut.model_validate(db_team)


@router.get("/{league_id}", status_code=status.HTTP_200_OK, response_model=schemas.Teams)
def get_league_teams(
    db: Session = Depends(get_db),
    league: models.League = Depends(get_current_league)
):
    teams = db.query(models.League).filter(
        models.League.id == league.id
    ).all()

    team_list = [schemas.TeamOut.model_validate(team) for team in teams]

    return schemas.Teams(teams=team_list)


