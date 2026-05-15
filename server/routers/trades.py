from routers import trade_engine
from fastapi import APIRouter, Depends, status, HTTPException
from models import models, schemas
import authentication.auth as auth

router = APIRouter(prefix="/leagues/{league_id}/teams/{team_id}/trade", tags=["Trades"])


@router.get("", status_code=status.HTTP_200_OK, response_model=schemas.TradeOut)
async def get_trades(team: models.Team = Depends(auth.get_current_players)):
    league = team.league
    teams = league.teams

    teams = [t for t in teams if t.id != team.id]

    if not teams:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No other teams to trade with",
        )

    team_list = [
        {"id": p.id, "name": p.name, "points": p.points_ppr, "position": p.position}
        for p in team.players
    ]
    if not team_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Team has no players to trade"
        )

    results = {}
    for t in teams:
        t_list = [
            {"id": p.id, "name": p.name, "points": p.points_ppr, "position": p.position}
            for p in t.players
        ]
        if t_list:
            trades = trade_engine.evaluate_trades(team_list, t_list)
            results[t.name] = [
                schemas.Trade(
                    players_1=[
                        schemas.TradePlayer(id=p[0], name=p[1])
                        for p in trade["team1_players"]
                    ],
                    gain_1=trade["team1_gain"],
                    players_2=[
                        schemas.TradePlayer(id=p[0], name=p[1])
                        for p in trade["team2_players"]
                    ],
                    gain_2=trade["team2_gain"],
                )
                for trade in trades
            ]

    return schemas.TradeOut(results)
