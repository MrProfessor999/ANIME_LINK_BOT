from animeSupport.database import db
import pymongo

collection = db.index


def addAnimes(animeList):
    collection.remove()
    collection.insert_many(animeList)
    collection.create_index([("name", pymongo.TEXT)])


def searchAnime(name):
    result = collection.find(
        {"$text": {"$search": name}},
        {"score": {"$meta": "textScore"}}
    ).sort([("score", {"$meta": "textScore"})])
    return result
