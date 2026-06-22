from backend.db import create_users_table, create_logs_table, add_user


def init():
    create_users_table()
    create_logs_table()

    add_user("alice", "alice123", "Finance")
    add_user("bob", "bob123", "Engineering")
    add_user("ceo", "ceo123", "C-Level")


if __name__ == "__main__":
    init()