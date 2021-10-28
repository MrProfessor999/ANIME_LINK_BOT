from pyrogram import __version__, filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputTextMessageContent, InlineQueryResultArticle, InlineQueryResultPhoto, InlineQuery

from animeSupport import bot
from animeSupport.helpers.msg_types import Types
from animeSupport.helpers.sauce import anime_sauce

# TODO: Add more inline query
# TODO: Wait for pyro update to add more inline query
GET_FORMAT = {
    Types.TEXT.value: InlineQueryResultArticle,
    # Types.DOCUMENT.value: InlineQueryResultDocument,
    Types.PHOTO.value: InlineQueryResultPhoto,
    # Types.VIDEO.value: InlineQueryResultVideo,
    # Types.STICKER.value: InlineQueryResultCachedSticker,
    # Types.AUDIO.value: InlineQueryResultAudio,
    # Types.VOICE.value: InlineQueryResultVoice,
    # Types.VIDEO_NOTE.value: app.send_video_note,
    # Types.ANIMATION.value: InlineQueryResultGif,
    # Types.ANIMATED_STICKER.value: InlineQueryResultCachedSticker,
    # Types.CONTACT: InlineQueryResultContact
}


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


@bot.on_inline_query()
async def inline_query_handler(client: Client, query: InlineQuery):
    string = query.query.lower()
    answers = []

    if string == "":
        await client.answer_inline_query(query.id,
                                         results=answers,
                                         switch_pm_text="Need help? Click here",
                                         switch_pm_parameter="help_inline"
                                         )
        return

    elif string.split()[0] == "anime":
        if len(string.split()) == 1:
            await client.answer_inline_query(query.id,
                                             results=answers,
                                             switch_pm_text="Search an Anime",
                                             switch_pm_parameter="help_inline"
                                             )
            return
        json = (await anime_sauce(string.split(None, 1)[1]))['data'].get('Page', None)
        if json:
            for data in json["media"]:
                info = data.get('siteUrl')
                trailer = data.get('trailer', None)
                if trailer:
                    trailer_id = trailer.get('id', None)
                    site = trailer.get('site', None)
                    if site == "youtube":
                        trailer = 'https://youtu.be/' + trailer_id

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
{shorten(description )}[.]({image})
'''

                answers.append(InlineQueryResultArticle(
                    title=f"{data['title']['romaji']}",
                    thumb_url=data['coverImage']['medium'],
                    description=f"{data['format']}({data['episodes']})",
                    input_message_content=InputTextMessageContent(
                        msg, parse_mode="markdown", disable_web_page_preview=False),
                ))
        await client.answer_inline_query(query.id,
                                         results=answers,
                                         cache_time=0
                                         )
