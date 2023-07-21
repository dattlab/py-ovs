import pymongo
import pymongo.database

from src.helpers import encrypt_passwd, passwd_match
from src.config import (
    MONGO_URI,
    DB_NAME,
    USER_COLLECTION_NAME,
    POLL_COLLECTION_NAME
)


class DBUtils:
    def __init__(
        self,
        mongo_uri: str = MONGO_URI,
        db_name: str = DB_NAME,
        user_collection_name: str = USER_COLLECTION_NAME,
        poll_collection_name: str = POLL_COLLECTION_NAME
    ) -> None:
        self.db = pymongo.MongoClient(mongo_uri)[db_name]
        self.user_collection = self.db[user_collection_name]
        self.poll_collection = self.db[poll_collection_name]

    def add_new_user(self, user_data: dict) -> None:
        if not self.username_in_db(user_data["username"]):
            user_data["passwd"] = encrypt_passwd(user_data["passwd"])
            self.user_collection.insert_one(user_data)

    def add_new_candidate(self, poll_name, candidate_name) -> None:
        if self.poll_exists(poll_name):
            new_candidate = {
                "candidate_name": candidate_name,
                "vote_count": 0
            }

            poll = self.poll_collection.find_one({"poll_name": poll_name})

            new_candidates_list = poll["candidates"].append(new_candidate)

            self.poll_collection.update_one({
                "_id": poll["_id"]
            }, {
                "$set": {
                    "candidates": new_candidates_list
                }
            }, upsert=False)

    def add_new_poll(self, poll_data: dict) -> None:
        self.poll_collection.insert_one(poll_data)

    def purge_collections(self) -> None:
        self.user_collection.delete_many({})
        self.poll_collection.delete_many({})

    def username_in_db(self, username: str) -> bool:
        return True if self.user_collection.find_one({"username": username}) \
            else False

    def poll_exists(self, poll_name: str) -> bool:
        return True if self.poll_collection.find_one({"poll_name": poll_name}) \
            else False

    def valid_credential(self, input_user_data: dict) -> bool:
        # Get the user entry from the database
        # that matches with input user data
        if self.username_in_db(input_user_data["username"]):
            stored_user_data = self.user_collection.find_one({
                "username": input_user_data["username"]
            })

            if passwd_match(input_user_data["passwd"], stored_user_data["passwd"]):
                return True

        return False
