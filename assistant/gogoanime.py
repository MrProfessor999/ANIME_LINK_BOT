from pyrogram.handlers import MessageHandler
from animeSupport.helpers.utils import async_call_later
from animeSupport.database.gogoanime import download_episode
from animeSupport import ANIME_HUB, ANIME_SUB, bot, AdminSettings, edrep, BITLY_TOKENS
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import FloodWait
from animeSupport.database import anime_search
from animeSupport.assistant.__main__ import addCallbackHandler, dynamic_data_filter, addHandler, removeHandler
import asyncio
from animeSupport.plugins import bitlyshortener
import uuid

__MODULE__ = "GoGo Anime"

__HELP__ = """
Module to upload files from gogo anime

──「 **Upload new** 」──
-> `gogo <anime>`
Send name of anime yuu want to upload.

"""

shortner = bitlyshortener.Shortener(tokens=BITLY_TOKENS, max_cache_size=256)


@bot.on_message(filters.user(AdminSettings) & filters.command(['gogo']) & filters.private)
async def Addnew(client: Client, message: Message):
    await asyncio.sleep(1)
    cmd = message.command
    mock = ""
    if len(cmd) > 1:
        mock = " ".join(cmd[1:])
    elif len(cmd) == 1:
        await edrep(message, text="`Format: gogo [anime name]`")
        await asyncio.sleep(2)
        await message.delete()
        return
    animes = anime_search(mock)

    if len(animes) > 0:
        for anime in animes:
            text = f"[.]({anime['img']})[.]({anime['link']}){anime['name']}"
            buttons = [[InlineKeyboardButton(
                "Upload", callback_data=f"gogo")]]
            await client.send_message(message.chat.id,
                                      text=text,
                                      disable_web_page_preview=False,
                                      reply_markup=InlineKeyboardMarkup(buttons))


@bot.on_callback_query(dynamic_data_filter('gogo'))
async def gogo(client, query: CallbackQuery):
    await asyncio.sleep(1)
    link = query.message.entities[-1].url
    name = query.message.text[2:]

    async def episodeFrom(client: Client, message: Message):
        removeHandler(handler)
        await gogoStage2(link, name, int(message.text), message)
    handler = addHandler(episodeFrom, query)

    await bot.send_message(query.message.chat.id, 'Enter starting episode (inclusive)')


async def gogoStage2(link, name, _from, message: Message):
    await asyncio.sleep(1)
    await message.reply_text("Enter ending episode (exclusive)")

    async def episodeTo(client: Client, message: Message):
        removeHandler(handler)
        await gogoStage3(link, name, _from, int(message.text), message)
    handler = addHandler(episodeTo, message)


async def gogoStage3(link, name, _from, to, message: Message):
    await asyncio.sleep(1)
    linkList = []
    for i in range(_from or 0, to or 0):
        try:
            downloadLink = download_episode(link, i)
            links = shortner.shorten_urls([downloadLink])
            _link = links[0] or downloadLink
            linkList.append({
                "episode": i,
                "link": _link,
                "name": _link.split('://')[-1]
            })
        except Exception:
            linkList.append({
                "episode": i,
                "link": downloadLink,
                "name": downloadLink.split('://')[-1] or "Can't get link"
            })
    UUID = uuid.uuid4()
    for item in linkList:
        await message.reply_text(f"Episode {str(item['episode']).zfill(2)}:\n{item['name']}")
    buttons = [[InlineKeyboardButton("Anime Hub", f"xgogohub_{UUID}"),
                InlineKeyboardButton("Anime Sub", f"xgogosub_{UUID}")],
               [InlineKeyboardButton("Other", f"xgogooth_{UUID}"),
               InlineKeyboardButton("Cancel", f"xgogocancel_{UUID}")]]
    msg = await message.reply_text("Should I forward this to channel", reply_markup=InlineKeyboardMarkup(buttons))

    async def anime_hub(client, query):
        removeHandler(anime_hub_handler)
        removeHandler(anime_sub_handler)
        removeHandler(anime_other_handler)
        removeHandler(cancel_handler)
        await gogoStage4(linkList, ANIME_HUB, "Anime Hub", query.message)

    async def anime_sub(client, query):
        removeHandler(anime_hub_handler)
        removeHandler(anime_sub_handler)
        removeHandler(anime_other_handler)
        removeHandler(cancel_handler)
        await gogoStage4(linkList, ANIME_SUB, "Anime Sub", query.message)

    async def anime_oth(client, query):
        removeHandler(anime_hub_handler)
        removeHandler(anime_sub_handler)
        removeHandler(anime_other_handler)
        removeHandler(cancel_handler)
        await gogoStage32(linkList, query.message)

    async def cancel(client, query: CallbackQuery):
        removeHandler(cancel_handler)
        removeHandler(anime_hub_handler)
        removeHandler(anime_other_handler)
        removeHandler(anime_sub_handler)
        await query.message.edit_text("Cancelled")

    anime_hub_handler = addCallbackHandler(
        anime_hub, f"xgogohub_{UUID}", message)
    anime_sub_handler = addCallbackHandler(
        anime_sub, f"xgogosub_{UUID}", message)
    anime_other_handler = addCallbackHandler(
        anime_oth, f"xgogooth_{UUID}", message)
    cancel_handler = addCallbackHandler(cancel, f"xgogocancel_{UUID}", message)

    async def callback():
        try:
            await msg.delete()
            removeHandler(anime_hub_handler)
            removeHandler(anime_sub_handler)
            removeHandler(anime_other_handler)
            removeHandler(cancel_handler)
        except Exception:
            pass
    async_call_later(1800, callback)


async def gogoStage32(linkList, message: Message):
    UUID = uuid.uuid4()
    buttons = [[InlineKeyboardButton('Cancel', f'cancel_{UUID}')]]
    msg = await message.edit_text("Add me as admin there wit post message privillage and forward me a message from that channel", reply_markup=InlineKeyboardMarkup(buttons))

    async def anime_other(client: Client, message: Message):
        removeHandler(cancel_handler)
        removeHandler(anime_other_handler)
        try:
            id = message.forward_from_chat.id
            info = await bot.get_chat(id)
            await gogoStage4(linkList, info.id, info.title, msg)
        except Exception as e:
            await msg.reply_text(f"Some error occured {e}")

    async def cancel(client, query: CallbackQuery):
        removeHandler(cancel_handler)
        removeHandler(anime_other_handler)
        await query.message.edit_text("Cancelled")

    cancel_handler = addCallbackHandler(cancel, f"cancel_{UUID}", message)
    anime_other_handler = bot.add_handler(MessageHandler(
        anime_other, filters.private & filters.forwarded))

    async def callback():
        try:
            await msg.delete()
            removeHandler(cancel_handler)
            removeHandler(anime_other_handler)
        except Exception:
            pass
    async_call_later(1800, callback)


async def gogoStage4(linkList, ID, channel, message: Message):
    UUID = uuid.uuid4()
    text = f'Sending message to {channel} do you want to proceed?'
    buttons = [[InlineKeyboardButton('Yes', f'yes_{UUID}'),
                InlineKeyboardButton('No', f'no_{UUID}')]]
    keyboard = InlineKeyboardMarkup(buttons)
    msg = await message.edit_text(text, reply_markup=keyboard)

    async def _yes(client, query):
        removeHandler(yes_handler)
        removeHandler(no_handler)
        await gogoStage5(linkList, ID, message)

    async def _no(client, query):
        removeHandler(yes_handler)
        removeHandler(no_handler)
        buttons = [[InlineKeyboardButton("Anime Hub", f"xgogohub_{UUID}"),
                    InlineKeyboardButton("Anime Sub", f"xgogosub_{UUID}")],
                   [InlineKeyboardButton("Cancel", f"xgogocancel_{UUID}")]]

        msg = await message.edit_text("Should I forward this to channel", reply_markup=InlineKeyboardMarkup(buttons))

        async def anime_hub(client, query):
            removeHandler(anime_hub_handler)
            removeHandler(cancel_handler)
            removeHandler(anime_sub_handler)
            await gogoStage4(linkList, ANIME_HUB, "Anime Hub", query.message)

        async def anime_sub(client, query):
            removeHandler(cancel_handler)
            removeHandler(anime_hub_handler)
            removeHandler(anime_sub_handler)
            await gogoStage4(linkList, ANIME_SUB, "Anime Sub", query.message)

        async def cancel(client, query: CallbackQuery):
            removeHandler(cancel_handler)
            removeHandler(anime_hub_handler)
            removeHandler(anime_sub_handler)
            await query.message.edit_text("Cancelled")

        anime_hub_handler = addCallbackHandler(
            anime_hub, f"xgogohub_{UUID}", message)
        anime_sub_handler = addCallbackHandler(
            anime_sub, f"xgogosub_{UUID}", message)
        cancel_handler = addCallbackHandler(
            cancel, f"xgogocancel_{UUID}", message)

        async def callback():
            try:
                await msg.delete()
                removeHandler(anime_hub_handler)
                removeHandler(cancel_handler)
                removeHandler(anime_sub_handler)
            except Exception:
                pass
        async_call_later(1800, callback)

    yes_handler = addCallbackHandler(_yes, 'yes', message)
    no_handler = addCallbackHandler(_no, 'no', message)

    async def callback():
        try:
            await msg.delete()
            removeHandler(yes_handler)
            removeHandler(no_handler)
        except Exception:
            pass
    async_call_later(1800, callback)


async def gogoStage5(linkList, ID, message: Message):
    for item in linkList:
        try:
            await bot.send_message(ID, f"Episode {str(item['episode']).zfill(2)}:\n{item['name']}")
        except FloodWait as e:
            await message.reply_text(f"Waiting {e.x} seconds to continue posting")
            await asyncio.sleep(e.x)
    await message.reply_text("Completed posting")
