import asyncio
from animeSupport.database.users import chatMode, checkChatMode
from animeSupport import BotID, MAIN_GROUP, bot
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

__MODULE__ = "Chat module"

__HELP__ = """
Module to chat between bot users and members in admin group.
Just reply to forwarded messages from bot.

"""


@bot.on_callback_query(filters.regex(r'^query$'))
async def query(client: Client, query: CallbackQuery):
    chatMode(query, True)
    text = """
__**To Ask a Query Please Write It Here :-**

Like If You Want To Know About
• Cross Promo
• Paid Promo
• Any Other Stuff__
    """
    buttons = [[KeyboardButton("Exit Chat Room")]]
    await query.message.delete()
    await query.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True))


@bot.on_message(filters.regex(r'^Exit Chat Room$'), group=1)
async def query(client: Client, message: Message):
    chatMode(message, False)
    buttons = [[InlineKeyboardButton("Go Back", "start")]]
    await message.reply_text("Leaving chat room.", reply_markup=ReplyKeyboardRemove())
    await message.reply_text("Admin can still respond to your query.", reply_markup=InlineKeyboardMarkup(buttons))


@bot.on_callback_query(filters.regex(r'^qyenter$'))
async def query(client: Client, query: CallbackQuery):
    await query.answer()
    chatMode(query, True)
    buttons = [[KeyboardButton("Exit Chat Room")]]
    await query.message.reply_text("Please write your reply", reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True))


@bot.on_message(filters.private, group=1)
async def chat(client: Client, message: Message):
    chatMode = checkChatMode(message)
    if chatMode and message.text != "/start":
        await message.forward(MAIN_GROUP)


@bot.on_message(filters.chat(MAIN_GROUP) & filters.reply, group=1)
async def replyChat(client: Client, message: Message):
    await asyncio.sleep(1)
    try:
        if message.reply_to_message.from_user.id == BotID:
            message.reply_to_message.from_user.id = message.reply_to_message.forward_from.id
            chatMode = checkChatMode(message.reply_to_message)
            keyboard = InlineKeyboardMarkup(
                [[InlineKeyboardButton("Enter Chat Room", "qyenter")]])
            if chatMode:
                keyboard = ReplyKeyboardMarkup(
                    [[KeyboardButton("Exit Chat Room")]], resize_keyboard=True, one_time_keyboard=True)
            await message.copy(message.reply_to_message.forward_from.id, reply_markup=keyboard)
    except Exception:
        await message.reply_text("Failed to contact user")
