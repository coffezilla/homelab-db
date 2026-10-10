from db import init_db, save_user


if __name__ == "__main__":
    init_db()
    print(save_user())
