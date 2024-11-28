import os
import psycopg2
import psycopg2.extras
from todolib.mytodo import *
from settings.config import db_name, user, password


class TodoUser:
    cur_user = None

    def __init__(self):
        self._connection = psycopg2.connect(
            dbname=db_name, user=user, password=password
        )
        self._cursor = self._connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor
        )
        self._connection.autocommit = True

        self.create_db_schema()

        self._cursor.execute("""SELECT COUNT(*) FROM users;""")
        self.q_users = self._cursor.fetchone()[0]

    def __del__(self):
        self._connection.close()
        self._cursor.close()

    def create_db_schema(self) -> None:
        self._cursor.execute(
            """CREATE TABLE IF NOT EXISTS users(
            username varchar(50) PRIMARY KEY NOT NULL, 
            password varchar(20) NOT NULL);"""
        )
        self._cursor.execute(
            """CREATE TABLE IF NOT EXISTS notes(
            id serial PRIMARY KEY, 
            username varchar(50) NOT NULL,
            text varchar
            );"""
        )

    def sign_up(self) -> bool:
        print("\nSign up: \n")
        username = str(input("Please enter your username >> "))
        password = str(input("Please enter your password >> "))

        if self.q_users != 0:
            self._cursor.execute("""SELECT * FROM users;""")
            for i in range(self.q_users):
                user_info = self._cursor.fetchone()
                if user_info["username"] == username:
                    print(
                        "\nError! a user with the same name already exists! Try again!\n"
                    )
                    return False

        self._cursor.execute(
            """INSERT INTO users (username, password)
            VALUES (%s, %s);""",
            (username, password),
        )
        self.q_users += 1
        self.cur_user = MyTodo(user=username, conn=self._connection, cur=self._cursor)
        print(f"You Success Sign Up!\n")
        return True

    def log_in(self) -> bool:
        print("Hello! Please sign in or sign up!\n")
        enter = str(input("[1] Sign in\n[2] Sign up\n>> "))

        if enter == "1":
            username = str(input("Username >> "))
            password = str(input("Password >> "))

            self._cursor.execute("""SELECT * FROM users;""")

            for i in range(self.q_users):
                user_info = self._cursor.fetchone()
                if (
                    user_info["username"] == username
                    and user_info["password"] == password
                ):
                    self.cur_user = MyTodo(
                        user=username, conn=self._connection, cur=self._cursor
                    )
                    print("succsess!")
                    return True
                elif (
                    user_info["username"] == username
                    and user_info["password"] != password
                ):
                    print("Wrong password! Please try again.\n")
                    return False
                else:
                    continue
            print("User not find! Please try again or sign up!\n")
            return False
        elif enter == "2":
            return self.sign_up()
        else:
            print("Invalid input!")
            return False
