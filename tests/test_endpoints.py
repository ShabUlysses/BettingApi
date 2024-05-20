import json


def test_get_bets(app_client, create_bet):
    response = app_client.get(f"/bets")
    bet = response.json()

    assert bet == create_bet


