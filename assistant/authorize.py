from animeSupport.__main__ import restart_all
from animeSupport.database.config import addAuthorizedUser, removeAuthorizedUser
from animeSupport.helpers.PyroHelpers import ReplyUserID
from animeSupport import SuperAdmins, bot
from pyrogram import Client, filters
from pyrogram.types import Message


__MODULE__ = "Authorize"

__HELP__ = """
Module to delegate access rights to other users.

──「 **Authorize** 」──
-> `authorize`
Send /authorize as a reply to the message of user whom you want to promote.
Make sure bot is member of that chat.

──「 **Deauthorize** 」──
-> `deauthorize`
Send /deauthorize as a reply to the message of user whom you want to demote.
Make sure bot is member of that chat.
"""


@bot.on_message(filters.user(SuperAdmins) & filters.command(['authorize']) & filters.reply)
async def authorize(client: Client, message: Message):
    id, mention = ReplyUserID(message)
    addAuthorizedUser(id)
    await restart_all()


@bot.on_message(filters.user(SuperAdmins) & filters.command(['deauthorize']) & filters.reply)
async def authorize(client: Client, message: Message):
    id, mention = ReplyUserID(message)
    removeAuthorizedUser(id)
    await restart_all()
