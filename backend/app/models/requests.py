from pydantic import BaseModel
from typing import Optional


class PlayRequest(BaseModel):
    speed: Optional[float] = None


class SpeedRequest(BaseModel):
    speed: float