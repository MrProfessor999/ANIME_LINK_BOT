class Config(object):
    LOGGER = True

    APP_ID = '7813081'
    API_HASH = 'deccd07c38a5ec9fa0fa6e58790fe292'
    BOT_TOKEN = '2034296193:AAHXmC1yQ8VycRLerTjYG7QRC8wSe6csdC0'
    ADMINS = [1296817425]
    ############################################################

    Command = ['!', '.']

    BOT_WORKER = 4

    BOT_LOAD = []
    BOT_NOLOAD = []

    PRIMARY_URL = "http://gogoanime.ai"
    SEARCH_URL = "/search.html?keyword="

    BITLY_TOKENS = [""]

    ANIME_HUB = 0
    ANIME_SUB = 0

    MAIN_GROUP = 0


class Production(Config):
    LOGGER = False


class Development(Config):
    LOGGER = True
