from db.utils import *


def main():
    user_taken = is_username_taken('user3')

    if user_taken:
        print(user_taken)
    else:
        print("MEH")


if __name__ == "__main__":
    main()
