import os
import re

from pyrogram import filters, Client
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram.types import Message

from animeSupport import bot


def dynamic_data_filter(data):
    async def func(flt, _, query):
        return bool(re.match(flt.data, query.data))

    # "data" kwarg is accessed with "flt.data" above
    return filters.create(func, data=data)


@bot.on_callback_query(dynamic_data_filter("report_errors"))
async def report_some_errors(client, query):
    await app.join_chat("@evabotsupport")
    text = "Hi, i got an error for you.\nPlease take a look and fix it if possible.\n\nThank you ❤️"
    err = query.message.text
    open("eva/cache/errors.txt", "w").write(err)
    await query.message.edit_reply_markup(reply_markup=None)
    await app.send_document("evabotsupport", "eva/cache/errors.txt", caption=text)
    os.remove("eva/cache/errors.txt")
    await client.answer_callback_query(query.id, "Report was sent!")


def addHandler(func, message):
    return bot.add_handler(MessageHandler(func, filters.private & filters.user(message.from_user.id)))


def removeHandler(handler):
    bot.remove_handler(*handler)


def addCallbackHandler(func, keyword, message):
    return bot.add_handler(CallbackQueryHandler(func, dynamic_data_filter(keyword)))


def addCommandHandler(func, command, message):
    return bot.add_handler(MessageHandler(func, filters.command([command]) & filters.private & filters.user(message.from_user.id)))
