from App.Database import db
from config import MongoCollections
from App.Util.constants import BREAKFAST, LUNCH
from App.Util.constants import CATERINGS


def get_menus(catering: str):
    if catering == BREAKFAST:
        collection_name = MongoCollections.MENUS_BREAKFAST
    elif catering == LUNCH:
        collection_name = MongoCollections.MENUS_LUNCH
    else:
        raise Exception(f"Invalid catering '{catering}' to get data into the database. Possible values: {CATERINGS}")

    return db.find_all(collection_name)
