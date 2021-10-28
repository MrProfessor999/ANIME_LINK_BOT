import asyncio
import re
from random import randrange
from animeSupport import bot
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from animeSupport.helpers.sauce import get_anime

__MODULE__ = "Feeling lucky"

__HELP__ = """
This module is for sending random anime to users who click **Feeling Lucky** button.

"""


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


@bot.on_callback_query(filters.regex(r'^lucky$'))
async def lucky(client: Client, query: CallbackQuery):
    await query.answer()
    await asyncio.sleep(1)
    id = [randrange(137041) for i in range(100)]
    json = (await get_anime(id))['data'].get('Page', None)
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
            buttons = [[InlineKeyboardButton("Go Back", "start2"),
                        InlineKeyboardButton("Feeling Lucky", f"lucky")]]

            await query.message.delete()
            await query.message.reply_photo(photo=image, caption=msg, reply_markup=InlineKeyboardMarkup(buttons))
        if len(json["media"]) == 0:
            buttons = [[InlineKeyboardButton("Go Back", 'start')]]
            await query.message.reply_text("You are unlucky now! try again", reply_markup=InlineKeyboardMarkup(buttons))
    else:
        await query.message.reply_text("Nothing found!")
