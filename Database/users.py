from animeSupport.database import db
from pyrogram.types import Message

collection = db.users


def newUser(msg: Message):
    user = {
        "_id": str(msg.from_user.id),
        "id": msg.from_user.id,
        "name": msg.from_user.first_name,
        "username": msg.from_user.username,
    }
    try:
        collection.insert_one(user)
    except Exception:
        pass


def chatMode(msg: Message, state: bool):
    collection.update_one({u'_id': str(msg.from_user.id)},
                          {"$set": {u'chatMode': state}})


def checkChatMode(msg: Message):
    result = collection.find_one({u'_id': str(msg.from_user.id)})
    if not result:
        return False
    return result.get('chatMode', False)
