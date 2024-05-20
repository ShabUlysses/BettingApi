from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, schemas
from .database import get_db

app = FastAPI()


@app.get("/bets")
async def get_bets(db: Session = Depends(get_db)):
    bets = crud.get_all_bets(db=db)
    if not bets:
        raise HTTPException(status_code=404, detail="No bets have been created yet")
    return bets


@app.post("/bets", response_model=schemas.BetResponse)
async def place_bet(bet: schemas.Bet, db: Session = Depends(get_db)):
    return crud.create_bet(db=db, event_id=bet.event_id, amount=bet.amount)


@app.put("/events/{event_id}", status_code=202)
async def update_event_status(
    event_id: str, new_status: str, db: Session = Depends(get_db)
):
    return crud.update_bets(db=db, event_id=event_id, status=new_status)
