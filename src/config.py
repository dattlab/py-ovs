from dotenv import dotenv_values

# For database
DB_NAME = "ovs"
USER_COLLECTION_NAME = "users"
CANDIDATE_COLLECTION_NAME = "candidates"
POS_COLLECTION_NAME = "positions"
MONGO_URI = dotenv_values("src/.env")["MONGO_URI"]
