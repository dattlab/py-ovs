from dotenv import dotenv_values


DB_NAME = "ovs"
USER_COLLECTION_NAME = "users"
MONGO_URI = dotenv_values(".env")['MONGO_URI']
