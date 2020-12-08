import traceback
from App.Database import db


def is_mongo_client_healthy() -> bool:
    """
    Returns True if the mongo connection is OK else returns False

    Returns:
        bool: Mongo's health
    """
    try:
        info = db.client_health()
        return bool(info)
    except Exception:
        traceback.print_exc()
        return False
