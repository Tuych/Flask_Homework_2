import sqlite3


class FDataBase:
    def __init__(self, con: object) -> object:
        self.__con = con
        self.__cur = con.cursor()

    def add_course(self, name, price, info):
        try:
            self.__cur.execute("INSERT INTO courses VALUES(NULL, ?, ?, ?)", (name, price, info))
            self.__con.commit()
            return True
        except sqlite3.Error as e:
            print('Ошибка добавлиния' + str(e))
            return False

    def get_course(self):
        sql = 'SELECT * FROM courses'
        try:
            res = self.__cur.execute(sql).fetchall()
            if res:
                return res

        except IOError:
            print("Ошибка чтиния и БД")
        return []

    def get_one_course(self, course_id):
        try:
            res = self.__cur.execute(f'SELECT * FROM courses WHERE id={course_id}').fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print('Ошибка получинея группа в БД' + str(e))

        return False
















