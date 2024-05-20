from sqlalchemy import Column, Integer, String

from .database import Base


class Bets(Base):
    __tablename__ = "bets"

    id = Column(Integer, primary_key=True)
    amount = Column(Integer, unique=False, index=False)
    event_id = Column(Integer, unique=False, index=False)
    uuid = Column(String(50), unique=False, index=False)
    bet_status = Column(String(50), unique=False, index=False)
