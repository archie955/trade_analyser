from routers import trade_engine
from fastapi import APIRouter, Depends, status, HTTPException
from models import models, schemas
import authentication.auth as auth

router = APIRouter(prefix="/leagues/{league_id}/teams/{team_id}/trade", tags=["Trades"])

@router.get("", status_code=status.HTTP_200_OK, response_model=dict)
async def get_trades(
    team: models.Team = Depends(auth.get_current_players)
):
    league = team.league
    teams = league.teams

    teams = [t for t in teams if t.id != team.id]

    if len(teams) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No other teams to trade with"
        )

    team_list = [
        {"id": p.id, "name": p.name, "points": p.points_ppr, "position": p.position} for p in team.players
    ]
    if len(team_list) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team has no players to trade"
        )

    results = {}
    for t in teams:
        t_list = [
            {"id": p.id, "name": p.name, "points": p.points_ppr, "position": p.position} for p in t.players
        ]
        if len(t_list) > 0:
            trades = trade_engine.evaluate_trades(team_list, t_list)
            results[t.name] = trades
    
    return results
