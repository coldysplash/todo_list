import os
from todolib.user import *


def show_menu():
    print("\n[1] Create new Todo\n" "[2] Delete Todo\n" "[3] Exit\n")


def main():
    try:
        os.system("clear")
        user = TodoUser()
    except Exception:
        print("Error! Can`t establish connection to Database!")
    else:
        if user.log_in():
            os.system("clear")
            print(f"Weclome {user.cur_user.username}!\n")
            while True:
                print("Your notes:\n")
                user.cur_user.show_tasks()
                show_menu()
                command = input(">> ")
                if command == "1":
                    os.system("clear")
                    user.cur_user.add_note()
                elif command == "2":
                    user.cur_user.del_note()
                elif command == "3":
                    exit()


if __name__ == "__main__":
    main()
