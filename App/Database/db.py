import pymongo
from typing import Dict, List
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.cursor import Cursor
from config import MONGO_STR_CONNECTION, MONGO_DB_NAME


class MongoManager:
    __client = None

    @staticmethod
    def get_client() -> MongoClient:
        """
        Gets a MongoClient instance for connecting with the data base

        Args:
            None

        Returns:
            MongoClient: Instance for connecting with the data base
        """
        if not MongoManager.__client:
            __client = pymongo.MongoClient(MONGO_STR_CONNECTION)
        return __client

    @staticmethod
    def get_game_collection(collection_name: str) -> Collection:
        """
        Gets a Database collection

        Args:
            collection_name (str): Collection name

        Returns:
            Collection: Database collection
        """
        client = MongoManager.get_client()
        db = client[MONGO_DB_NAME]
        return db[collection_name]


def client_health() -> MongoClient:
    """
    Gets a MongoClient instance with the server information

    Args:
        None

    Returns:
        MongoClient: Connectivity server information
    """
    client = MongoManager.get_client()
    return client.server_info()


def find_one_by_id(id_document: str, collection_name: str) -> Dict:
    """
    Gets a document given a id and a collection name

    Args:
        id_document (str): Mongo document identifier (_id)
        collection_name (str): Collection to search the element

    Raises:
        Exception: If the element was not found

    Returns:
        Dict: Mongo document
    """
    collection = MongoManager.get_game_collection(collection_name)
    document = collection.find_one({'_id': id_document})
    if not document:
        raise Exception(f'Game {id_document} not found on "{collection_name}" collection')
    return document


def find_all(collection_name: str) -> Cursor:
    """
    Gets all the documents from a collection

    Args:
        collection_name (str): Collection to search the element

    Returns:
        Cursor: Mongo cursor
    """
    collection = MongoManager.get_game_collection(collection_name)
    cursor = collection.find({})
    return cursor


def add_one(document: Dict, collection_name: str) -> None:
    """
    Insets a new document into a collection

    Args:
        document (Dict): Document to save
        collection_name (str): Collection to search the element

    Returns:
        None
    """
    collection = MongoManager.get_game_collection(collection_name)
    collection.insert_one(document)


def add_many(documents: List[Dict], collection_name: str) -> None:
    """
    Insets a new document into a collection

    Args:
        documents (Dict): List of documents to save
        collection_name (str): Collection to search the element

    Returns:
        None
    """
    collection = MongoManager.get_game_collection(collection_name)
    collection.insert_many(documents)


def update_one_by_id(id_document: str, dict_updates: Dict, collection_name: str, upsert: bool = False) -> None:
    """
    Updates a document in a collection

    Args:
        id_document (str): Mongo document identifier (_id)
        dict_updates (Dict): Document updates
        collection_name (str): Collection to search the element
        upsert (bool): True for creating a new record if the document does not match with the filter query

    Returns:
        None
    """
    collection = MongoManager.get_game_collection(collection_name)
    query = {'_id': id_document}
    updates = {'$set': dict_updates}
    collection.update_one(query, updates, upsert)


def delete_one(search_field: str, search_value: str, collection_name: str) -> None:
    """
    Removes a game from the Database

    Args:
        search_field (str): Field to identify the document
        search_value (str): Value to identify the document
        collection_name (str): Collection to search the element

    Returns:
        None
    """
    collection = MongoManager.get_game_collection(collection_name)
    collection.delete_one({search_field: search_value})


def delete_many(search_field: str, search_value: str, collection_name: str) -> None:
    """
    Removes a game from the Database

    Args:
        search_field (str): Field to identify the document
        search_value (str): Value to identify the document
        collection_name (str): Collection to search the element

    Returns:
        None
    """
    collection = MongoManager.get_game_collection(collection_name)
    collection.delete_many({search_field: search_value})
