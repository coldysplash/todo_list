import psycopg2
import psycopg2.extras


class MyTodo:
    TodoInfo = []
    username = ""
    _connection = None
    _cursor = None

    def __init__(self, user, conn, cur):
        self.username = user
        self._connection = conn
        self._cursor = cur
        self._cursor.execute("""SELECT COUNT(%s) FROM notes;""", (self.username,))
        self.t_lenght = self._cursor.fetchone()[0]
        self.select_info()

    def __del__(self):
        self._connection.close()
        self._cursor.close()

    def select_info(self):
        self._cursor.execute(
            """SELECT * FROM notes WHERE username=%s;""", (self.username,)
        )
        for i in range(self.t_lenght):
            notes = self._cursor.fetchone()
            self.TodoInfo.append(notes["text"])

    def add_note(self) -> None:
        todo = str(input("Inpput New Todo >> "))
        self._cursor.execute(
            """INSERT INTO notes (username, text) 
            VALUES (%s, %s);""",
            (self.username, todo),
        )
        self.TodoInfo.append(todo)
        self.t_lenght += 1

    def del_note(self) -> None:
        if self.t_lenght == 0:
            return
        idx = int(input("What todo you wanna delete? Input number >> "))
        if idx < 1 or idx > self.t_lenght:
            print("Sorry! Invalid index.\n")
            return

        self._cursor.execute(
            """DELETE FROM notes WHERE text=%s;""", (self.TodoInfo[idx - 1],)
        )
        self.TodoInfo.pop(idx - 1)
        self.t_lenght -= 1

    def show_tasks(self):
        for i in range(len(self.TodoInfo)):
            print(f"[{i + 1}] {self.TodoInfo[i]}")
