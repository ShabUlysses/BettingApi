from uuid import uuid4
import json
import pytest
from sqlalchemy_utils import create_database, database_exists
from fastapi.testclient import TestClient
from app.database import create_session, Base
from app.models import Bets
from app import app
from app.crud import BetStatus


class TestSettings:
    DATABASE_URL = "postgresql://user:password@localhost:5432/db-test"


@pytest.fixture(scope="session")
def db(session_mocker):
    session_mocker.patch("app.database.get_settings", return_value=TestSettings())
    db_session = create_session()
    engine = db_session.bind
    if not database_exists(engine.url):
        create_database(engine.url)
    Base.metadata.bind = engine
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    return db_session


@pytest.fixture()
def cleanup_db(db):
    for table in reversed(Base.metadata.sorted_tables):
        db.execute(table.delete())


@pytest.fixture()
def app_client(cleanup_db):
    yield TestClient(app=app.app)


@pytest.fixture()
def mock_uuid(app_client):
    data = {"event_id": 2, "amount": 500}
    response = app_client.post("/bets", data=json.dumps(data))
    uuid = response.json()["uuid"]
    yield uuid


@pytest.fixture()
def create_bet(db):
    bet = Bets(
        event_id=2, amount=500, uuid=str(uuid4()), bet_status=BetStatus.PENDING.value
    )
    db.add(bet)
    db.commit()
    yield bet
