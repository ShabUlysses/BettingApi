import json


def test_get_no_bets(app_client):
    response = app_client.get("/bets")

    assert response.status_code == 404


def test_get_bets(app_client, create_bet):
    response = app_client.get("/bets")
    bet = response.json()

    assert bet == [
        {
            "amount": create_bet.amount,
            "bet_status": create_bet.bet_status,
            "event_id": create_bet.event_id,
            "id": create_bet.id,
            "uuid": create_bet.uuid,
        }
    ]


def test_place_bet(app_client, create_bet):
    data = {"event_id": 2, "amount": 500}
    response = app_client.post("/bets", data=json.dumps(data))
    bet = response.json()

    assert len(bet["uuid"]) == len(create_bet.uuid)


def test_update_event_won(app_client, create_bet):
    response = app_client.put(f"/events/{2}", params={"new_status": "WIN"})
    assert response.status_code == 202
    assert create_bet.bet_status == "выиграла"


def test_update_event_lost(app_client, create_bet):
    response = app_client.put(f"/events/{2}", params={"new_status": "LOSE"})
    assert response.status_code == 202
    assert create_bet.bet_status == "проиграла"
