from backend.database.schema import DBAccount

def test_get_nonexistent_account(session, client):
    session.add(DBAccount(username="chatty"))
    session.commit()

    response = client.get("/accounts/100")
    assert response.status_code == 404
    assert response.json() == {"entity_not_found": "Unable to find account with id=100"}

def test_get_accounts(session, client):
    chatty = "chatty"
    yappy = "yappy"
    session.add(DBAccount(username=chatty))
    session.add(DBAccount(username=yappy))
    session.commit()

    response = client.get("/accounts")
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": chatty},
        {"id": 1, "name": yappy}
    ]

def test_get_account_1(session, client):
    chatty = "chatty"
    yappy = "yappy"
    session.add(DBAccount(username=chatty))
    session.add(DBAccount(username=yappy))
    session.commit()

    response = client.get("/accounts/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": chatty}

def test_get_account_2(session, client):
    chatty = "chatty"
    yappy = "yappy"
    session.add(DBAccount(username=chatty))
    session.add(DBAccount(username=yappy))
    session.commit()

    response = client.get("/accounts/2")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": yappy}