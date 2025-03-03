from backend.database.schema import DBAccount

def test_get_nonexistent_account(session, client):
    chatty = "chatty"
    yappy = "yappy"
    chatty_email = "chatty@email.com"
    yappy_email = "yappy@email.com"
    chatty_password = "chatty123"
    yappy_password = "yappy321"
    
    session.add(DBAccount(username=chatty, email=chatty_email, hashed_password = chatty_password))
    session.add(DBAccount(username=yappy, email=yappy_email, hashed_password = yappy_password))
    session.commit()

    response = client.get("/accounts/100")
    assert response.status_code == 404
    assert response.json() == {"error": "entity_not_found", "message": "Unable to find account with id=100"}

def test_get_accounts(session, client):
    chatty = "chatty"
    yappy = "yappy"
    chatty_email = "chatty@email.com"
    yappy_email = "yappy@email.com"
    chatty_password = "chatty123"
    yappy_password = "yappy321"
    
    session.add(DBAccount(username=chatty, email=chatty_email, hashed_password = chatty_password))
    session.add(DBAccount(username=yappy, email=yappy_email, hashed_password = yappy_password))
    session.commit()

    response = client.get("/accounts")
    assert response.status_code == 200
    assert response.json() == {
        "metadata": {"count": 2},
        "accounts": [
            {"id": 1, "username": chatty},
            {"id": 2, "username": yappy}
        ]
    }

def test_get_account_1(session, client):
    chatty = "chatty"
    yappy = "yappy"
    chatty_email = "chatty@email.com"
    yappy_email = "yappy@email.com"
    chatty_password = "chatty123"
    yappy_password = "yappy321"
    
    session.add(DBAccount(username=chatty, email=chatty_email, hashed_password = chatty_password))
    session.add(DBAccount(username=yappy, email=yappy_email, hashed_password = yappy_password))
    session.commit()

    response = client.get("/accounts/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "username": chatty}

def test_get_account_2(session, client):
    chatty = "chatty"
    yappy = "yappy"
    chatty_email = "chatty@email.com"
    yappy_email = "yappy@email.com"
    chatty_password = "chatty123"
    yappy_password = "yappy321"
    
    session.add(DBAccount(username=chatty, email=chatty_email, hashed_password = chatty_password))
    session.add(DBAccount(username=yappy, email=yappy_email, hashed_password = yappy_password))
    session.commit()

    response = client.get("/accounts/2")
    assert response.status_code == 200
    assert response.json() == {"id": 2, "username": yappy}