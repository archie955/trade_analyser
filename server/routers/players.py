from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from models import models, schemas
from database.database import get_db
from models.datatypes import Positions
from authentication.auth import get_current_league

router = APIRouter(
    prefix="/players/{league_id}", tags=["Players"]
)

@router.get("", status_code=status.HTTP_200_OK, response_model=schemas.Players)
async def fetch_players(
    free_agent: bool = False,
    pos: Positions | None = None,
    asc: bool = False,
    skip: int | None = None,
    limit: int | None = None,
    db: AsyncSession = Depends(get_db),
    league: models.League = Depends(get_current_league)
):
    stmt = f"SELECT p.*, tp.team_id AS team_id FROM players p LEFT JOIN team_players tp ON (p.id = tp.player_id) WHERE (tp.team_id IS NULL OR tp.league_id = {league.id})"
    if free_agent:
        stmt += " AND tp.team_id IS NULL"
    if pos:
        stmt += f" AND p.pos = {pos}"
    if asc:
        stmt += " ORDER BY p.points_ppr"
    else:
        stmt += " ORDER BY p.points_ppr DESC"
    if limit:
        stmt += f" LIMIT {limit}"
    if skip:
        stmt += f" OFFSET {skip}"

    players = (
        await db.execute(text(stmt))
    ).scalars().all()

    print(players)

    players_list = [schemas.PlayersOut.model_validate(player) for player in players]

    return schemas.Players(players=players_list)


