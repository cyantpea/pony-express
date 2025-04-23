from sqlmodel import Session, select

from backend.database.schema import DBChat, DBMessage, DBAccount, DBChatMembership
from backend.exceptions import ChatMembershipRequired, ChatOwnerRemoval, EntityNotFound, DuplicateEntity
from backend.models.chats import ChatCreate, ChatUpdate, ChatMembershipCreate, ChatMembership, MessageCreate, MessageUpdate
from backend.database import accounts as db_accounts

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

def get_by_name(session: Session, name: str) -> DBChat | None:
    """Retrieve specific chat from database.
    
    Args:
        session (Session): The database session
        name (str): The name of the chat to retrieve
    
    Returns:
        DBChat: The chat
    """
    
    return session.exec(select(DBChat).where(DBChat.name == name)).first()

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
    
    chat = get_by_id(session, chat_id)
    stmt = select(DBMessage).where(DBMessage.chat_id == chat_id)
    results = session.exec(stmt)
    return list(results)

def create_chat(session: Session, chat: ChatCreate) -> DBChat:
    """Create a new chat in the database.
    
    Args:
        session (Session): The database session
        chat (ChatCreate): The chat to create
        
    Returns:
        DBChat: The created chat
        
    Raises:
        EntityNotFound: If no account with given id exists
        DuplicateEntity: If the chat name already exists
    """

    user = db_accounts.get_by_id(session, chat.owner_id)

    duplicate_chat = get_by_name(session, chat.name)
    if (duplicate_chat):
        raise DuplicateEntity(chat.name)
    
    db_chat = DBChat(
        name=chat.name,
        owner_id=user.id,
    )

    membership = DBChatMembership(
        account_id=user.id,
        chat=db_chat,
    )

    db_chat.memberships.append(membership)

    session.add(db_chat)
    session.commit()
    session.refresh(db_chat)

    return db_chat

def update_chat(session: Session, chat_id: int, chat: ChatUpdate) -> DBChat:
    """Update a chat in the database.
    
    Args:
        session (Session): The database session
        chat_id (int): The id of the chat
        chat (ChatUpdate): The updated chat
        
    Returns:
        DBChat: The updated chat
        
    Raises:
        EntityNotFound: If no chat with given id exists
        ChatMembershipRequired: If the account is not a member of the chat or does not exist
        DuplicateEntity: If the chat name already exists
    """
    
    updated_chat = get_by_id(session, chat_id)

    if (chat.owner_id):
        account = session.get(DBAccount, chat.owner_id)
        accounts = get_accounts_for_chat(session, chat_id)
        if account is None or not any(acc.id == chat.owner_id for acc in accounts):
            raise ChatMembershipRequired(chat.owner_id, chat_id)
        setattr(updated_chat, "owner_id", chat.owner_id)

    if (chat.name):
        duplicate_chat = get_by_name(session, chat.name)
        if (duplicate_chat):
            raise DuplicateEntity(chat.name)
        setattr(updated_chat, "name", chat.name)
    
    session.commit()
    session.refresh(updated_chat)
    return updated_chat

def delete_chat(session: Session, chat_id: int):
    """Delete a chat from the database.
    
    Args:
        session (Session): The database session
        chat_id (int): The id of the chat to delete
        
    Raises:
        EntityNotFound: If no chat with given id exists
    """
    
    chat = get_by_id(session, chat_id)
    messages = session.exec(select(DBMessage).where(DBMessage.chat_id == chat_id)).all()
    memberships = session.exec(select(DBChatMembership).where(DBChatMembership.chat_id == chat_id)).all()

    for msg in messages:
        session.delete(msg)

    for membership in memberships:
        session.delete(membership)

    session.delete(chat)

    session.commit()
    
def add_message(session: Session, chat_id: int, message: MessageCreate) -> DBMessage:
    """Add a message to a chat.
    
    Args:
        session (Session): The database session
        chat_id (int): The id of the chat
        message (MessageCreate): The message to add
        
    Returns:
        DBMessage: The created message
        
    Raises:
        EntityNotFound: If no chat with given id exists
        ChatMembershipRequired: If the account is not a member of the chat or does not exist
    """
    
    chat = get_by_id(session, chat_id)

    account = session.get(DBAccount, message.account_id)
    accounts = get_accounts_for_chat(session, chat_id)
    if account is None or not any(acc.id == message.account_id for acc in accounts):
        raise ChatMembershipRequired(message.account_id, chat_id)
    
    new_message = DBMessage(text=message.text, account_id=message.account_id, chat_id=chat_id)

    session.add(new_message)
    session.commit()

    return new_message

def update_message(session: Session, chat_id: int, message_id: int, message: MessageUpdate) -> DBMessage:
    """Update a message in a chat.
    
    Args:
        session (Session): The database session
        chat_id (int): The id of the chat
        message_id (int): The id of the message to update
        message (MessageUpdate): The updated message
        
    Returns:
        DBMessage: The updated message
        
    Raises:
        EntityNotFound: If no chat with given id exists
        EntityNotFound: If no message with given id exists
    """

    chat = get_by_id(session, chat_id)
    messages = get_messages_for_chat(session, chat_id)

    existing_message = session.get(DBMessage, message_id)
    if existing_message is None or not any(msg.id == message_id for msg in messages):
        raise EntityNotFound("message", message_id)
    
    setattr(existing_message, "text", message.text)

    session.commit()
    session.refresh(existing_message)

    return existing_message
    
def delete_message(session: Session, chat_id: int, message_id: int):
    """Delete a message from a chat.
    
    Args:
        session (Session): The database session
        chat_id (int): The id of the chat
        message_id (int): The id of the message to delete
        
    Raises:
        EntityNotFound: If no chat with given id exists
        EntityNotFound: If no message with given id exists
    """
    
    chat = get_by_id(session, chat_id)
    message = session.exec(select(DBMessage).where(DBMessage.id == message_id)).first()
    
    if not message or message.chat_id != chat_id:
        raise EntityNotFound("message", message_id)
    
    session.delete(message)
    session.commit()

def add_membership(session: Session, chat_id: int, chat_membership: ChatMembershipCreate) -> DBChatMembership:
    """Add a membership to a chat.
    
    Args:
        session (Session): The database session
        chat_id (int): The id of the chat
        chat_membership (ChatMembershipCreate): The membership to add
        
    Returns:
        DBChatMembership: The created membership
        
    Raises:
        EntityNotFound: If no chat with given id exists
        EntityNotFound: If no account with given id exists
    """
    
    chat = get_by_id(session, chat_id)
    account = db_accounts.get_by_id(session, chat_membership.account_id)
    
    membership = DBChatMembership(account_id=chat_membership.account_id, chat_id=chat_id)
    session.add(membership)
    session.commit()
    return membership

def get_membership_by_ids(session: Session, chat_id: int, account_id: int) -> DBChatMembership | None:
    """Retrieve a specific membership from the database.
    
    Args:
        session (Session): The database session
        chat_id (int): The id of the chat
        account_id (int): The id of the account

    Returns:
        DBChatMembership: The membership

    """

    return session.exec(select(DBChatMembership).filter_by(chat_id=chat_id, account_id=account_id)).first()

def delete_membership(session: Session, chat_id: int, account_id: int):
    """Delete a membership from a chat.
    
    Args: 
        session (Session): The database session
        chat_id (int): The id of the chat
        account_id (int): The id of the account
        
    Raises:
        EntityNotFound: If no chat with given id exists
        EntityNotFound: If no account with given id exists
        ChatMembershipRequired: If the account is not a member of the chat
        ChatOwnerRemoval: If trying to remove the owner of the chat
    """

    chat = get_by_id(session, chat_id)
    account = db_accounts.get_by_id(session, account_id)
    membership = get_membership_by_ids(session, chat_id, account_id)

    if not membership or not account:
        raise ChatMembershipRequired(account_id=account_id, chat_id=chat_id)

    if chat.owner_id == account_id:
        raise ChatOwnerRemoval()
    
    messages = session.exec(select(DBMessage).filter_by(chat_id=chat_id, account_id=account_id))
    for msg in messages:
        setattr(msg, "account_id", None)
    
    session.delete(membership)
    session.commit()
