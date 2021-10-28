import re
import time

from __main__ import HELP_COMMANDS  # pylint: disable-msg=E0611
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram.raw import functions

from animeSupport import bot, AdminSettings, Command, BotUsername
from animeSupport.__main__ import BOT_RUNTIME
from animeSupport.helpers.misc import paginate_modules


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        remainder, result = divmod(
            seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "
    time_list.reverse()
    ping_time += ":".join(time_list)
    return ping_time


async def help_parser(client, chat_id, text, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(
            paginate_modules(0, HELP_COMMANDS, "help"))
    await client.send_message(chat_id, text, reply_markup=keyboard)


@bot.on_message(filters.user(AdminSettings) & filters.command(["help"]))
async def help_command(client, message):
    if message.chat.type != "private":
        buttons = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Help",
                                   url=f"t.me/{BotUsername}?start=help")]])
        await message.reply("Contact me in PM to get the list of possible commands.",
                            reply_markup=buttons)
        return
    await help_parser(client, message.chat.id, "Available commands")


@bot.on_message(filters.private & filters.command(['help']))
async def help_public_command(client: Client, message: Message):
    text = """
ᗯᗩᑎᎢ ᗩ ᗷᝪᎢ ᏞᏆᏦᗴ ᎢᕼᏆᔑ

✨𝔞𝔱 𝔩𝔬𝔴𝔢𝔰𝔱 𝔭𝔬𝔰𝔰𝔦𝔟𝔩𝔢 𝔥𝔬𝔲𝔯𝔩𝔶 𝔠𝔥𝔞𝔯𝔤𝔢
✨𝔣𝔯𝔢𝔢 𝔬𝔫𝔢 𝔶𝔢𝔞𝔯 𝔡𝔢𝔭𝔩𝔬𝔶𝔪𝔢𝔫𝔱

🧑‍💻ᴄᴏɴᴛᴀᴄᴛ @Kaori_autobot
    """
    buttons = [[InlineKeyboardButton("Go Back",'start2')]]
    await message.reply_text(text,reply_markup=InlineKeyboardMarkup(buttons))


async def help_button_callback(_, __, query):
    if re.match(r"help_", query.data):
        return True


help_button_create = filters.create(help_button_callback)


@bot.on_callback_query(help_button_create)
async def help_button(_client, query):
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)
    if mod_match:
        module = mod_match.group(1)
        text = "This is help for the module **{}**:\n".format(HELP_COMMANDS[module].__MODULE__) \
               + HELP_COMMANDS[module].__HELP__

        await query.message.edit(text=text,
                                 reply_markup=InlineKeyboardMarkup(
                                     [[InlineKeyboardButton(text="Back", callback_data="help_back")]]))

    elif back_match:
        await query.message.edit("Available commands",
                                 reply_markup=InlineKeyboardMarkup(paginate_modules(0, HELP_COMMANDS, "help")))
