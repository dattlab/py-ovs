import json
import random
import pymongo
import pymongo.database

from src.helpers import encrypt_passwd, passwd_match
from src.config import (
    MONGO_URI,
    DB_NAME,
    USER_COLLECTION_NAME,
    POS_COLLECTION_NAME
)


class DBUtils:
    def __init__(
            self,
            mongo_uri: str = MONGO_URI,
            db_name: str = DB_NAME,
            user_collection_name: str = USER_COLLECTION_NAME,
            position_collection_name: str = POS_COLLECTION_NAME
    ) -> None:
        self.db = pymongo.MongoClient(mongo_uri)[db_name]
        self.user_collection = self.db[user_collection_name]
        self.position_collection = self.db[position_collection_name]

    def add_new_user(self, name: str, username: str, passwd: str) -> None:
        global voter_id

        voter_id_in_db = self.get_all_voters_id()

        if not self.username_in_db(username):
            passwd = encrypt_passwd(passwd)

            # Create random 5-digit voter ID
            voter_id_already_in_db = True
            while voter_id_already_in_db:
                voter_id = random.randint(10000, 99999)
                if voter_id not in voter_id_in_db:
                    voter_id_already_in_db = False

            self.user_collection.insert_one({
                "name"        : name,
                "username"    : username,
                "passwd"      : passwd,
                "voter_id"    : voter_id,
                "is_admin"    : False,
                "vote_history": []
            })

    def add_new_candidate(self, position_name: str, candidate_name: str) -> None:
        if self.position_exists(position_name):
            new_candidate = {
                "candidate_name": candidate_name,
                "vote_count"    : 0
            }

            pos = self.position_collection.find_one({"position_name": position_name})

            new_candidates_list = pos["candidates"]
            new_candidates_list.append(new_candidate)

            self.position_collection.update_one({
                "_id": pos["_id"]
            }, {
                "$set": {
                    "candidates": new_candidates_list
                }
            }, upsert=False)

    def update_candidate_vote_count(self, position_name: str, candidate_name: str) -> None:
        pos = self.position_collection.find_one({
            "position_name"            : position_name,
            "candidates.candidate_name": candidate_name
        })

        self.position_collection.update_one({
            "_id"                      : pos["_id"],
            "candidates.candidate_name": candidate_name
        }, {
            "$inc": {
                "candidates.$.vote_count": 1
            }
        })

    def update_vote_history(self, username: str, position_name: str, candidate_name: str) -> None:
        self.update_candidate_vote_count(position_name, candidate_name)

        candidate = self.user_collection.find_one({"username": username})

        vote_history = candidate["vote_history"]

        vote_history.append({
            "pos_name"        : position_name,
            "chosen_candidate": candidate_name
        })

        self.user_collection.update_one({
            "_id": candidate["_id"]
        }, {
            "$set": {
                "vote_history": vote_history
            }
        }, upsert=False)

    def add_new_pos(self, position_data: dict) -> None:
        self.position_collection.insert_one(position_data)

    def get_all_voters_id(self) -> list[int]:
        users = list(self.user_collection.find({}))
        voter_id_list = []
        for user in users:
            if not user["is_admin"]:
                voter_id_list.append(user["voter_id"])

        return voter_id_list

    def import_collection_from_json(self, json_file_path: str, collection_name: str) -> None:
        with open(json_file_path, "r") as f:
            documents = json.loads(f.read())

        self.db[collection_name].insert_many(documents)

    def purge_collections(self) -> None:
        self.user_collection.delete_many({})
        self.position_collection.delete_many({})

    def user_already_voted(self, position_name: str, username: str) -> bool:
        user_vote_history = self.user_collection.find_one({"username": username})

        # List of positions where the user already voted in
        pos_voted = [v["pos_name"] for v in user_vote_history["vote_history"]]

        if position_name in pos_voted:
            return True

        return False

    def user_is_admin(self, username: str) -> bool:
        user = self.user_collection.find_one({"username": username})
        if user["is_admin"]:
            return True
        return False

    def username_in_db(self, username: str) -> bool:
        return True if self.user_collection.find_one({"username": username}) \
            else False

    def position_exists(self, position_name: str) -> bool:
        return True if self.position_collection.find_one({"position_name": position_name}) \
            else False

    def valid_credential(self, username: str, passwd: str) -> bool:
        # Get the user entry from the database
        # that matches with input user data
        if self.username_in_db(username):
            stored_user_data = self.user_collection.find_one({
                "username": username
            })

            if passwd_match(passwd, stored_user_data["passwd"]):
                return True

        return False
