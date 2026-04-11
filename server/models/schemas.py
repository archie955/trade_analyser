from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List
from datetime import datetime

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

class LeagueOut(LeagueCreate):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = config

class LeagueUpdate(LeagueCreate):
    id: int

class Leagues(BaseModel):
    leagues: List[LeagueOut]

# TEAMS