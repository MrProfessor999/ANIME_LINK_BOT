from pyrogram.types import User, Message


def ReplyCheck(message):
    reply_id = None
    if message.reply_to_message:
        reply_id = message.reply_to_message.message_id
    elif not message.from_user.is_self:
        reply_id = message.message_id
    return reply_id


def GetUserMentionable(user: User):
    "Get mentionable text of a user."
    if user.username:
        username = "@{}".format(user.username)
    else:
        if user.last_name:
            name_string = "{} {}".format(user.first_name, user.last_name)
        else:
            name_string = "{}".format(user.first_name)
        username = "<a href='tg://user?id={}'>{}</a>".format(
            user.id, name_string)
    return username


def ReplyUserID(message: Message):
    if message.reply_to_message:
        return message.reply_to_message.from_user.id, message.reply_to_message.from_user.mention
    return 0, 'No one'
