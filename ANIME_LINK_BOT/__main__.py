import asyncio
import importlib
import time

from pyrogram import idle

from animeSupport import bot, get_bot
from animeSupport.assistant import ALL_SETTINGS

BOT_RUNTIME = 0
HELP_COMMANDS = {}

loop = asyncio.get_event_loop()


async def get_runtime():
    return BOT_RUNTIME


async def reinitial_restart():
    await get_bot()


async def reboot():
    global BOT_RUNTIME, HELP_COMMANDS
    importlib.reload(importlib.import_module("animeSupport.assistant"))
    # await bot.send_message(Owner, "Bot is restarting...")
    await bot.restart()
    await reinitial_restart()
    # Reset global var
    BOT_RUNTIME = 0
    HELP_COMMANDS = {}
    # Assistant bot
    for setting in ALL_SETTINGS:
        imported_module = importlib.import_module(
            "animeSupport.assistant." + setting)
        if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
            imported_module.__MODULE__ = imported_module.__MODULE__
        if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
            if imported_module.__MODULE__.lower() not in HELP_COMMANDS:
                HELP_COMMANDS[imported_module.__MODULE__.lower()
                              ] = imported_module
            else:
                raise Exception(
                    "Can't have two modules with the same name! Please change one")
        if hasattr(imported_module, "__HELP__") and imported_module.__HELP__:
            HELP_COMMANDS[imported_module.__MODULE__.lower()] = imported_module
        importlib.reload(imported_module)


async def restart_all():
    # Restarting and load all plugins
    asyncio.get_event_loop().create_task(reboot())


async def reinitial():
    await bot.start()
    await get_bot()
    await bot.stop()


async def start_bot():
    # sys.excepthook = except_hook
    print("----- Checking bot... -----")
    await reinitial()
    print("----------- Check done! ------------")
    # Assistant bot
    await bot.start()
    for setting in ALL_SETTINGS:
        imported_module = importlib.import_module(
            "animeSupport.assistant." + setting)
        if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
            imported_module.__MODULE__ = imported_module.__MODULE__
        if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
            if imported_module.__MODULE__.lower() not in HELP_COMMANDS:
                HELP_COMMANDS[imported_module.__MODULE__.lower()
                              ] = imported_module
            else:
                raise Exception(
                    "Can't have two modules with the same name! Please change one")
        if hasattr(imported_module, "__HELP__") and imported_module.__HELP__:
            HELP_COMMANDS[imported_module.__MODULE__.lower()] = imported_module

    assistant_modules = ""
    j = 1
    for i in ALL_SETTINGS:
        if j == 4:
            assistant_modules += "|{:<15}|\n".format(i)
            j = 0
        else:
            assistant_modules += "|{:<15}".format(i)
        j += 1

    print("+===============================================================+")
    print("|                    Assistant Modules                          |")
    print("+===============+===============+===============+===============+")
    print(assistant_modules)
    print("+===============+===============+===============+===============+")
    print("Bot run successfully!")

    await idle()


if __name__ == '__main__':
    BOT_RUNTIME = int(time.time())
    loop.run_until_complete(start_bot())
