from animeSupport.database import db

collection = db.config


def addAuthorizedUser(id):
    collection.update_one({"key": "AdminUsers"},
                          {"$addToSet": {"ids": id}},
                          upsert=True)


def removeAuthorizedUser(id):
    collection.update_one({"key": "AdminUsers"}, {"$pull": {"ids": id}})


def getAuthorizedUsers():
    result = collection.find_one({"key": "AdminUsers"})
    if not result:
        return []
    return result["ids"] or []
