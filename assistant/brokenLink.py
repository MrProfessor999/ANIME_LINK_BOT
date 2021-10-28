from animeSupport import bot
from animeSupport.database.users import chatMode
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup

__MODULE__ = "Broken link"

__HELP__ = """
Module to report broken links to members in admin group.
Just reply to forwarded messages from bot.

"""


@bot.on_callback_query(filters.regex(r'^broken_link$'))
async def brokenLink(client: Client, query: CallbackQuery):
    await query.answer()
    chatMode(query, True)
    text = """
__**To Report a Broken/Dead link 🔗 :-**

Please Forward The Link To This Bot Or Write The Episode Number And Name Of The Anime__
    """
    buttons = [[KeyboardButton("Exit Chat Room")]]
    await query.message.delete()
    await query.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True))
