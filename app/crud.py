from enum import Enum

from sqlalchemy.orm import Session

from . import models, schemas
from uuid import uuid4


class BetStatus(Enum):
    PENDING = 'ещё не сыграла'
    WIN = 'выиграла'
    LOSE = 'проиграла'


def get_all_bets(db: Session):
    return db.query(models.Bets).order_by(models.Bets.id.asc()).all()


def create_bet(db: Session, event_id: int, amount: int):
    bet_status = BetStatus.PENDING.value
    db_bet = models.Bets(event_id=event_id, amount=amount, uuid=str(uuid4()), bet_status=bet_status)
    db.add(db_bet)
    db.commit()
    return db_bet


def update_bets(db: Session, event_id: str, status: str):
    bet_status = BetStatus.WIN.value if status == "WIN" else BetStatus.LOSE.value
    bets = db.query(models.Bets).filter(models.Bets.event_id == event_id).all()
    for bet in bets:
        bet.bet_status = bet_status
    db.commit()
    return 202, "Successful"
