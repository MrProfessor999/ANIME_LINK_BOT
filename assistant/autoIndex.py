import asyncio
from animeSupport.database.index import addAnimes
from animeSupport.helpers.string import extractLinks
from pyrogram import Client, filters
from pyrogram.types import Message

from animeSupport import INDEX_CHANNELS, INDEX_CHANNEL_OFFSETS, MAIN_GROUP, bot, AdminSettings

__MODULE__ = "Auto Indexing"

__HELP__ = """
Module to perform auto indexing and update index in bot database.
Triggered automatically upon changes in index channels.

"""


@bot.on_message(filters.chat(INDEX_CHANNELS))
async def autoIndex(client: Client, message: Message):
    await asyncio.sleep(1)
    try:
        await client.send_message(MAIN_GROUP, "Updating index")
        indexes = []
        for count in range(len(INDEX_CHANNELS)):
            msg = await client.send_message(INDEX_CHANNELS[count], "Updated index", disable_notification=True)
            lastIndex = msg.message_id
            await msg.delete()
            for i in range(INDEX_CHANNEL_OFFSETS[count], lastIndex, 200):
                stop = i+200
                if stop > lastIndex:
                    stop = lastIndex
                msgs = await client.get_messages(INDEX_CHANNELS[count], range(i, stop))
                for msg in msgs:
                    if not msg.empty and msg.entities:
                        indexes.extend(extractLinks(msg))

        addAnimes(indexes)
        await client.send_message(MAIN_GROUP, "Updated index")
    except Exception as e:
        await client.send_message(MAIN_GROUP, "Index updating failed")
        await client.send_message(MAIN_GROUP, str(e))
