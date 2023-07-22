from src.db.utils import DBUtils
from src.ui.app import VotingSystem


DB = DBUtils()


def main():
    app = VotingSystem()
    app.run()


if __name__ == "__main__":
    main()
