from src.ui.app import VotingSystem
# from src.db.utils import DBUtils


def main():
    app = VotingSystem()
    app.run()

    # db = DBUtils()
    # db.purge_collections()
    # db.import_collection_from_json("src/data/positions.json", "positions")
    # db.import_collection_from_json("src/data/users.json", "users")


if __name__ == "__main__":
    main()
