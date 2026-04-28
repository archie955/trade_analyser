from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List
from datetime import datetime
import datatypes

config = ConfigDict(from_attributes=True)

# USERS

class User(BaseModel):
    email: EmailStr
    username: str

class UserCreate(User):
    password: str

class UserOut(User):
    model_config = config
    id: int
    created_at: datetime
    updated_at: datetime

class UserUpdate(BaseModel):
    updated_user: UserCreate
    password: str

# TOKENS

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]

# LEAGUES

class LeagueCreate(BaseModel):
    name: str

class LeagueUpdate(LeagueCreate):
    id: int

class LeagueOut(LeagueUpdate):
    created_at: datetime
    updated_at: datetime
    model_config = config

class Leagues(BaseModel):
    leagues: List[LeagueOut]

# TEAMS

class TeamCreate(BaseModel):
    name: str

class TeamUpdate(TeamCreate):
    id: int

class TeamOut(TeamUpdate):
    league_id: int
    created_at: datetime
    updated_at: datetime
    model_config = config

class Teams(BaseModel):
    teams: List[TeamOut]

# PLAYERS

class PlayerOut(BaseModel):
    id: int
    name: str
    team: datatypes.Teams
    position: datatypes.Positions
    points_ppr: float
    points_halfppr: float
    points_noppr: float
    model_config = config

class TeamPlayers(BaseModel):
    players: List[PlayerOut]
    model_config = config


# TRADES

class TradePlayer(BaseModel):
    id: int
    name: str
    model_config = config

class Trade(BaseModel):
    players_1: List[TradePlayer]
    gain_1: float
    payers_2: List[TradePlayer]
    gain_2: float
    model_config = config

class Trades(BaseModel):
    name: str
    trades: List[Trade]
    model_config = config

class TradeOut(BaseModel):
    trades: List[Trades]
    model_config = config