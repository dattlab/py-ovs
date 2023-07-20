# Third party modules
import pymongo as mongo

# User modules
from .config import (
    MONGO_URI,
    DB_NAME,
    USER_COLLECTION_NAME
)


def get_database(db_name: str = DB_NAME) -> mongo.database.Database:
    """
    Connects to a MongoClient with provided Mongo
    URI connection string and returns a database

    Parameters
    ----------
    db_name : str

    Returns
    -------
    mongo.database.Database

    """
    client = mongo.MongoClient(MONGO_URI)

    return client[db_name]


def get_collection(
        collection_name: str,
        db_name = DB_NAME
    ) -> mongo.collection.Collection:
    """
    Get a collection from a given database name

    Parameters
    ----------
    collection_name : str

    Returns
    -------
    mongo.collection.Collection

    """

    db_name = get_database(db_name)
    collection = db_name[collection_name]

    return collection


def insert_new_user(user_data: dict) -> None:
    """
    Insert new user to users collection

    Parameters
    ----------
    user_data: dict
        
    """
    user_collection = get_collection(USER_COLLECTION_NAME)
    user_collection.insert_one(user_data)


def is_username_taken(input_username: str) -> bool:
    """
    Checks if a user in data list
    is already in the given collection

    Parameters
    ----------
    data_list : dict

    Returns
    -------
    bool
        
    """

    user_collection = get_collection(USER_COLLECTION_NAME)

    return True if user_collection.find_one({
                    'username': input_username
                }) \
                else False

