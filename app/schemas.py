from pydantic import BaseModel


class Bet(BaseModel):
    event_id: int
    amount: int


class BetResponse(BaseModel):
    uuid: str
    class Config:
        orm_mode = True
