class Config(object):
    LOGGER = True

    APP_ID = 46372547
    API_HASH = 'pdhsghfhfgjsfhaghgfhjfasjgj'
    BOT_TOKEN = '1377736365:AAEFwpa-GGEne5XHyxYAK4wbw7P17BdaDmaM'
    ADMINS = []
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
