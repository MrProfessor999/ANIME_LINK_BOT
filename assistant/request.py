from animeSupport.database.index import searchAnime
from animeSupport.helpers.utils import async_call_later
from pyrogram.types.bots_and_keyboards.inline_keyboard_button import InlineKeyboardButton
from animeSupport.helpers.sauce import anime_search
from animeSupport.assistant.__main__ import addHandler, removeHandler
from animeSupport import MAIN_GROUP, bot

from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InputMediaPhoto

import asyncio
import re


def shorten(description, info='anilist.co'):
    ms_g = ""
    if len(description) > 700:
        description = description[0:500] + '..'
    ms_g += f"**Description**: __{description}__"
    return (
        ms_g.replace("<br>", "")
        .replace("</br>", "")
        .replace("<i>", "")
        .replace("</i>", "")
    )


@bot.on_callback_query(filters.regex(r'^request$'))
async def request(client: Client, query: CallbackQuery):
    await asyncio.sleep(1)
    text = """
__**To Request An Anime :-**

✨Enter It's Name/Title In English Please 🏷️ 

✨When The Result You Want Comes Press   **I Want This Anime**

✨Please Don't Request Hentai/18+ Content Or Else You Might Get Banned 🚫__
    """
    await query.edit_message_text(text)

    async def search_anime(client: Client, message: Message):
        removeHandler(handler)
        await requestStage2(message)
    handler = addHandler(search_anime, query)

    async def callback():
        try:
            await query.message.delete()
            removeHandler(handler)
        except Exception:
            pass
    async_call_later(1800, callback)


async def requestStage2(message: Message):
    await asyncio.sleep(1)
    name = re.sub(r'[^a-zA-Z0-9\s]*', '', message.text)
    json = (await anime_search(name, 1))['data'].get('Page', None)
    if json:
        for data in json["media"]:
            description = data.get('description', 'N/A') or 'N/A'
            description = description.replace('<i>', '').replace(
                '</i>', '').replace('<br>', '')
            image = f'https://img.anili.st/media/{data["id"]}'
            msg = f'''
**{data['title']['romaji']}** (`{data['title']['native']}`)
**Type**: {data['format']}
**Status**: {data['status']}
**Episodes**: {data.get('episodes', 'N/A')}
**Duration**: {data.get('duration', 'N/A')} Per Ep.
**Score**: {data['averageScore']}
**Genres**: `{', '.join(data["genres"])}`
**Studios**: `{', '.join([x['name'] for x in data['studios']['nodes']])}`
{shorten(description )}
    '''
            pageInfo = json['pageInfo']
            navigator = []
            if(pageInfo['currentPage'] != pageInfo['lastPage']):
                navigator.append(InlineKeyboardButton(
                    "Next", f'xq_2_{name}'))
            buttons = []
            if len(navigator):
                buttons.append(navigator)
            buttons.append([InlineKeyboardButton("Go Back", 'start'),
                            InlineKeyboardButton("I Want This Anime", f"xqm_{data['id']}_{name}")])

            await message.reply_photo(photo=image, caption=msg, reply_markup=InlineKeyboardMarkup(buttons))
        if len(json["media"]) == 0:
            buttons = [[InlineKeyboardButton("Go Back", 'start')]]
            await message.reply_text("Nothing found!", reply_markup=InlineKeyboardMarkup(buttons))
    else:
        await message.reply_text("Nothing found!")


@bot.on_callback_query(filters.regex(r'xq_([0-9]+)_(.*)'))
async def requestStage3(client: Client, query: CallbackQuery):
    await asyncio.sleep(1)
    await query.answer()
    page = int(query.matches[0].group(1))
    name = query.matches[0].group(2)
    json = (await anime_search(name, page))['data'].get('Page', None)
    if json:
        for data in json["media"]:
            description = data.get('description', 'N/A') or 'N/A'
            description = description.replace('<i>', '').replace(
                '</i>', '').replace('<br>', '')
            image = f'https://img.anili.st/media/{data["id"]}'
            msg = f'''
**{data['title']['romaji']}** (`{data['title']['native']}`)
**Type**: {data['format']}
**Status**: {data['status']}
**Episodes**: {data.get('episodes', 'N/A')}
**Duration**: {data.get('duration', 'N/A')} Per Ep.
**Score**: {data['averageScore']}
**Genres**: `{', '.join(data["genres"])}`
**Studios**: `{', '.join([x['name'] for x in data['studios']['nodes']])}`
{shorten(description )}
    '''
            pageInfo = json['pageInfo']
            navigator = []
            if(pageInfo['currentPage'] != 1):
                navigator.append(InlineKeyboardButton(
                    "Previous", f'xq_{page-1}_{name}'))
            if(pageInfo['currentPage'] != pageInfo['lastPage']):
                navigator.append(InlineKeyboardButton(
                    "Next", f'xq_{page+1}_{name}'))
            buttons = []
            if len(navigator):
                buttons.append(navigator)
            buttons.append([InlineKeyboardButton("Go Back", "start"),
                            InlineKeyboardButton("I Want This Anime", f"xqm_{data['id']}_{name}")])

            media = InputMediaPhoto(image, msg)
            await query.message.edit_media(media, reply_markup=InlineKeyboardMarkup(buttons))
        if len(json["media"]) == 0:
            buttons = [[InlineKeyboardButton("Go Back", 'start')]]
            await query.message.reply_text("Nothing found!", reply_markup=InlineKeyboardMarkup(buttons))
    else:
        await query.message.reply_text("Nothing found!")


@bot.on_callback_query(filters.regex(r'^xqm_([0-9]+)_(.*)'))
async def requestStage4(client: Client, query: CallbackQuery):
    await asyncio.sleep(1)
    await query.answer()
    animeID = query.matches[0].group(1)
    name = query.matches[0].group(2)
    result = searchAnime(name)
    buttons = []
    for anime in result:
        buttons.append([InlineKeyboardButton(
            anime["name"].strip(), url=anime["link"])])
    if len(buttons) == 0:
        await requestStage5(client, query)
        return

    buttons.append([InlineKeyboardButton("*It's Here 😊 *", "start"),
                    InlineKeyboardButton("*No, It's Not Here 😔 *", f"xqf_{animeID}_{name}")])
    await query.edit_message_text("**Is This The Anime You Want ?**", reply_markup=InlineKeyboardMarkup(buttons))


@bot.on_callback_query(filters.regex(r'^xqf_(.*)_(.*)'))
async def requestStage5(client: Client, query: CallbackQuery):
    await asyncio.sleep(1)
    await query.answer()
    animeID = query.matches[0].group(1)
    name = query.matches[0].group(2)
    image = f'https://img.anili.st/media/{animeID}'
    text = f"""
**[Request]({image})**

**Name:**  __{query.from_user.mention}__
**Username:** __{query.from_user.username}__
**Anime:** __{name}__
    """
    buttons = [[InlineKeyboardButton("Go Back", "start2")]]
    await bot.send_message(MAIN_GROUP, text, disable_web_page_preview=False)
    await query.edit_message_text("\n\n**Requested successfully**\n\n", reply_markup=InlineKeyboardMarkup(buttons))
