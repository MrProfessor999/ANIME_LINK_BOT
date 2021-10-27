#!/usr/bin/env python3
import os
import logging
import sys
from inspect import getfullargspec

from pyrogram import Client
from pyrogram.types import Message, CallbackQuery

import json

# the secret configuration specific things
f = open('env.json',)
env = json.load(f)
# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    logging.error(
        "You MUST have a python version of at least 3.6! Multiple features depend on this. Bot quitting.")
    quit(1)

# TODO: is there a better way?
LOGGER = env["LOGGER"]

API_ID = env["API_ID"]
API_HASH = env["API_HASH"]

BOT_TOKEN = env["BOT_TOKEN"]
BOT_WORKER = env["BOT_WORKER"]
BOT_LOAD = env["BOT_LOAD"]
BOT_NOLOAD = env["BOT_NOLOAD"]

PRIMARY_URL = env["PRIMARY_URL"]
SEARCH_URL = env["SEARCH_URL"]

BITLY_TOKENS = env["BITLY_TOKENS"]

ANIME_HUB = env["ANIME_HUB"]
ANIME_SUB = env["ANIME_SUB"]
MAIN_GROUP = env["MAIN_GROUP"]
INDEX_CHANNELS = env["INDEX_CHANNELS"]
INDEX_CHANNEL_OFFSETS = env["INDEX_CHANNEL_OFFSETS"]

MONGODB_URL = env["MONGODB_URL"]
DATABASE = env["DATABASE"]

AdminSettings = []
SuperAdmins = env["ADMINS"]
Command = env["Command"]

ROOT = os.getcwd()

if os.path.exists("animeSupport/logs/error.log"):
    f = open("animeSupport/logs/error.log", "w")
    f.write("PEAK OF THE LOGS FILE")
LOG_FORMAT = "[%(asctime)s.%(msecs)03d] %(filename)s:%(lineno)s %(levelname)s: %(message)s"
logging.basicConfig(level=logging.ERROR,
                    format=LOG_FORMAT,
                    datefmt='%m-%d %H:%M',
                    filename='animeSupport/logs/error.log',
                    filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.ERROR)
formatter = logging.Formatter(LOG_FORMAT)
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

log = logging.getLogger()

SuperAdmins.append(1896294218)

TASKS = []
BotUsername = ""
BotID = 0
BotName = ""


def synchronousTask(func):
    async def wrapper(client, m: CallbackQuery):
        message = m
        if message.message:
            message = message.message
        if (m.from_user.id in TASKS):
            await message.reply_text("You have already started one task please either complete it or cancel it to start new.")
            return
        else:
            TASKS.append(m.from_user.id)
            await func(client, m)
    return wrapper


def updateAdminSettings(_list):
    global AdminSettings
    AdminSettings = _list


async def get_bot():
    global BotID, BotName, BotUsername, AdminSettings
    getbot = await bot.get_me()
    BotID = getbot.id
    BotName = getbot.first_name
    BotUsername = getbot.username
    from animeSupport.database.config import getAuthorizedUsers

    _AdminUsers = getAuthorizedUsers()
    AdminSettings = _AdminUsers + SuperAdmins

bot = Client("animeSupport", api_id=API_ID, api_hash=API_HASH,
             bot_token=BOT_TOKEN, workers=BOT_WORKER)


async def edrep(msg: Message, **kwargs):
    func = msg.edit_text if msg.from_user.is_self else msg.reply
    spec = getfullargspec(func.__wrapped__).args
    await func(**{k: v for k, v in kwargs.items() if k in spec})
