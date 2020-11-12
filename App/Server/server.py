import traceback

from App.database import db


def is_mongo_client_healthy() -> bool:
    try:
        info = db.client_health()
        return bool(info)
    except Exception:
        traceback.print_exc()
        return False
