from routers import trade_engine
from fastapi import APIRouter, Depends, status
from models import models, schemas
import authentication.auth as auth

router = APIRouter(prefix="/trades", tags=["Trades"])

@router.get("/{league_id}/{team_id}", status_code=status.HTTP_200_OK, response_model=dict)
def get_trades(
    team: models.Team = Depends(auth.get_current_team)
):
    league = team.league
    teams = league.teams

    def filter_func(t):
        if t.id == team.id:
            return False
        return True
    
    teams = filter(filter_func, teams)

    team_list = []

    for player in team.players:
        player_dict = {"id": player.id, "name": player.name, "points": player.points_ppr, "position": player.position}
        team_list.append(player_dict)

    results = {}
    for t in teams:
        t_list = []
        for p in t.players:
            p_dict = {"id": p.id, "name": p.name, "points": p.points_ppr, "position": p.position}
            t_list.append(p_dict)
        trades = trade_engine.evaluate_trades(team_list, t_list)

        results[t.name] = trades
    
    return results
