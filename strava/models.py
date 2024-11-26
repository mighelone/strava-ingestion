import datetime

from pydantic import BaseModel


class StravaAthelete(BaseModel):
    id: int
    username: str
    resource_state: int
    firstname: str
    lastname: str
    city: str
    state: str
    country: str
    sex: str
    premium: bool
    summit: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
    badge_type_id: int
    weight: float
    profile_medium: str
    profile: str
    friend: str | None = None
    follower: str | None = None


class StravaToken(BaseModel):
    token_type: str
    expires_at: int
    expires_in: int
    refresh_token: str
    access_token: str
    athlete: StravaAthelete | None = None


# class RefreshToken(BaseModel):
#     token_type: str
#     access_token: str
#     expires_in: int
#     expires_at: int
#     refresh_token: str
