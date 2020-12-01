from typing import List, Dict
from App.Database import db, collection_manager


def get_list_menu_docs(catering: str) -> List[Dict]:
    collection_name: str = collection_manager.get_menu_collection(catering)
    return [document for document in db.find_all(collection_name)]


def get_list_register_docs(catering: str) -> List[Dict]:
    collection_name: str = collection_manager.get_register_collection(catering)
    return [document for document in db.find_all(collection_name)]


def get_dataset_docs(catering: str) -> List[Dict]:
    collection_name: str = collection_manager.get_database_collection(catering)
    return [document for document in db.find_all(collection_name)]
