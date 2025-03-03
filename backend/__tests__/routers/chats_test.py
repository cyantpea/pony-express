from backend.database.schema import DBAccount, DBChat, DBMessage

def test_get_nonexistent_chat(session, client):
    session.add(DBChat(name="chatty", owner_id=1))
    session.commit()

    response = client.get("/chats/100")
    assert response.status_code == 404
    assert response.json() == {"error": "entity_not_found", "message": "Unable to find chat with id=100"}

def test_get_chats(session, client):
    chatty = "chatty"
    yappy = "yappy"

    session.add(DBChat(name=chatty, owner_id=1))
    session.add(DBChat(name=yappy, owner_id=2))
    session.commit()

    response = client.get("/chats")
    assert response.status_code == 200
    assert response.json() == {
        "metadata": {"count": 2},
        "chats": [
            {"id": 1, "name": chatty, "owner_id": 1},
            {"id": 2, "name": yappy, "owner_id": 2}
        ]
    }

def test_get_chat_1(session, client):
    chatty = "chatty"
    yappy = "yappy"

    session.add(DBChat(name=chatty, owner_id=1))
    session.add(DBChat(name=yappy, owner_id=2))
    session.commit()

    response = client.get("/chats/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": chatty, "owner_id": 1}

def test_get_chat_2(session, client):
    chatty = "chatty"
    yappy = "yappy"

    session.add(DBChat(name=chatty, owner_id=1))
    session.add(DBChat(name=yappy, owner_id=2))
    session.commit()

    response = client.get("/chats/2")
    assert response.status_code == 200
    assert response.json() == {"id": 2, "name": yappy, "owner_id": 2}