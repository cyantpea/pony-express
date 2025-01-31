from sqlmodel import Session, select

from backend.database.schema import DBChat, DBMessage, DBAccount, DBChatMembership
from backend.exceptions import EntityNotFound

def get_all(session: Session) -> list[DBChat]:
    """Retrieve all chats from database.
    
    Args:
        session (Session): The database session
    
    Returns:
        list[DBChat]: The list of chats
    """

    stmt = select(DBChat)
    results = session.exec(stmt)
    return list(results)

def get_by_id(session: Session, chat_id: int) -> DBChat:
    """Retrieve specific chat from database.
    
    Args:
        session (Session): The database session
        chat_id (int): The id of the chat to retrieve
    
    Returns:
        DBChat: The chat

    Raises:
        EntityNotFound: If no chat with given id exists
    """
    
    chat = session.get(DBChat, chat_id)
    if chat is None:
        raise EntityNotFound("chat", chat_id)
    return chat

def get_accounts_for_chat(session: Session, chat_id: int) -> list[DBAccount]:
    """Retrieve all accounts for a chat in the database.
    
    Args:
        session (Session): The database session
        chat_id (int): The id of the chat
    
    Returns:
        list[DBAccount]: The list of accounts belonging to chat

    Raises:
        EntityNotFound: If no chat with given id exists
    """
    
    chat = session.get(DBChat, chat_id)
    if chat is None:
        raise EntityNotFound("chat", chat_id)
    stmt = select(DBAccount).join(DBChatMembership).where(DBChatMembership.chat_id == chat_id)
    results = session.exec(stmt)
    return list(results)

def get_messages_for_chat(session: Session, chat_id: int) -> list[DBMessage]:
    """Retrieve all messages for a chat in the database.
    
    Args:
        session (Session): The database session
        chat_id (int): The id of the chat
    
    Returns:
        list[DBMessage]: The list of messages belonging to chat

    Raises:
        EntityNotFound: If no chat with given id exists
    """
    
    chat = session.get(DBChat, chat_id)
    if chat is None:
        raise EntityNotFound("chat", chat_id)
    stmt = select(DBMessage).where(DBMessage.chat_id == chat_id)
    results = session.exec(stmt)
    return list(results)