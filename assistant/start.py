from animeSupport.database.users import newUser
from pyrogram.types.bots_and_keyboards.callback_query import CallbackQuery
from pyrogram.types.input_media.input_media import InputMedia
from pyrogram.types.input_media.input_media_photo import InputMediaPhoto
from animeSupport import bot

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

text = """
__**Welcome To Anime Support Bot**

**This Bot Will Help You To :-**
- Make Requests For Anime
- Ask Queries
- Report Broken/Dead Links

**How To Use This Bot :-**

✨If You Want To Request an Anime Then Press Request Button

✨If You Want To Ask a Query Then Press Query Button

✨If You Want To Report a Broken Link Then Press Broken Link Button

✨If You Want a Random Anime Press Feeling Lucky Button

🚫Please Refrain From Spamming Or Else You Might Get Banned Permanently

**Please Choose From Below**__
"""
buttons = [[InlineKeyboardButton("Request", "request"),
            InlineKeyboardButton("Query", "query")],
           [InlineKeyboardButton("Broken Link", "broken_link"),
            InlineKeyboardButton("Feeling lucky", "lucky")]]
keyboard = InlineKeyboardMarkup(buttons)


@bot.on_message(filters.private & filters.command(['start']))
async def start(client: Client, message: Message):
    newUser(message)
    await message.reply_text(text, reply_markup=keyboard, parse_mode='md')


@bot.on_callback_query(filters.regex(r'^start$'))
async def start_callback(client: Client, query: CallbackQuery):
    await query.answer()
    await query.message.delete()
    await query.message.reply_text(text, reply_markup=keyboard)


@bot.on_callback_query(filters.regex(r'^start2$'))
async def start_callback(client: Client, query: CallbackQuery):
    await query.answer()
    await query.message.reply_text(text, reply_markup=keyboard)
