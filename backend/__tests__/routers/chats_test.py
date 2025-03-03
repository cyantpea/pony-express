from backend.database.schema import DBAccount, DBChat, DBMessage, DBChatMembership
from datetime import datetime

def test_get_nonexistent_chat(session, client):
    session.add(DBChat(name="chatty", owner_id=1))
    session.commit()

    response = client.get("/chats/100")
    assert response.status_code == 404
    assert response.json() == {"error": "entity_not_found", "message": "Unable to find chat with id=100"}

def test_get_nonexistent_chat_messages(session, client):
    chatty = "chatty"
    yappy = "yappy"
    time = datetime.now()
    time_str = time.isoformat()

    session.add(DBChat(name=chatty, owner_id=1))
    session.add(DBChat(name=yappy, owner_id=2))
    session.add(DBMessage(id=1, text=chatty, account_id=1, chat_id=1, created_at=time))
    session.add(DBMessage(id=2, text=yappy, account_id=1, chat_id=1, created_at=time))
    session.commit()

    response = client.get("/chats/100/messages")
    assert response.status_code == 404
    assert response.json() == {"error": "entity_not_found", "message": "Unable to find chat with id=100"}

def test_get_nonexistent_chat_accounts(session, client):
    chatty = "chatty"
    yappy = "yappy"
    chatty_email = "chatty@email.com"
    yappy_email = "yappy@email.com"
    chatty_password = "chatty123"
    yappy_password = "yappy321"

    
    session.add(DBChat(id=1, name=chatty, owner_id=1))
    session.add(DBChat(id=2, name=yappy, owner_id=2))
    session.add(DBAccount(username=chatty, email=chatty_email, hashed_password = chatty_password))
    session.add(DBAccount(username=yappy, email=yappy_email, hashed_password = yappy_password))
    session.add(DBChatMembership(account_id=1, chat_id=1))
    session.add(DBChatMembership(account_id=2, chat_id=1))
    session.add(DBChatMembership(account_id=1, chat_id=2))
    session.add(DBChatMembership(account_id=2, chat_id=2))
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

def test_get_messages(session, client):
    chatty = "chatty"
    yappy = "yappy"
    time = datetime.now()
    time_str = time.isoformat()

    session.add(DBChat(name=chatty, owner_id=1))
    session.add(DBChat(name=yappy, owner_id=2))
    session.add(DBMessage(id=1, text=chatty, account_id=1, chat_id=1, created_at=time))
    session.add(DBMessage(id=2, text=yappy, account_id=1, chat_id=1, created_at=time))
    session.commit()

    response = client.get("/chats/1/messages")
    assert response.status_code == 200
    assert response.json() == {
        "metadata": {"count": 2},
        "messages": [
            {"id": 1, "text": chatty, "account_id": 1, "chat_id": 1, "created_at": time_str},
            {"id": 2, "text": yappy, "account_id": 1, "chat_id": 1, "created_at": time_str}
        ]
    }

def test_get_chat_accounts(session, client):
    chatty = "chatty"
    yappy = "yappy"
    chatty_email = "chatty@email.com"
    yappy_email = "yappy@email.com"
    chatty_password = "chatty123"
    yappy_password = "yappy321"

    
    session.add(DBChat(id=1, name=chatty, owner_id=1))
    session.add(DBChat(id=2, name=yappy, owner_id=2))
    session.add(DBAccount(username=chatty, email=chatty_email, hashed_password = chatty_password))
    session.add(DBAccount(username=yappy, email=yappy_email, hashed_password = yappy_password))
    session.add(DBChatMembership(account_id=1, chat_id=1))
    session.add(DBChatMembership(account_id=2, chat_id=1))
    session.add(DBChatMembership(account_id=1, chat_id=2))
    session.add(DBChatMembership(account_id=2, chat_id=2))
    session.commit()

    response = client.get("/chats/1/accounts")
    assert response.status_code == 200
    assert response.json() == {
        "metadata": {"count": 2},
        "accounts": [
            {"id": 1, "username": chatty},
            {"id": 2, "username": yappy}
        ]
    }
