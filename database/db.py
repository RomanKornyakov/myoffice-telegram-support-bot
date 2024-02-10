import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def get_questions(self):  # создание словаря с вопросами из базы данных
        with self.connection:
            result = self.cursor.execute('select id, questions from support').fetchall()
            data = {}

            for row in result:
                questions = tuple(row[1].split('/'))
                data[row[0]] = questions

            return data

    def get_answer(self, answer_id):  # получение ответа на вопрос пользователя
        with self.connection:
            return self.cursor.execute('select answer from support where id = ?', (answer_id,)).fetchone()[0]

    def view_data_in_support(self):  # просмотр данных в таблице support
        with self.connection:
            return self.cursor.execute('select * from support').fetchall()

    def view_data_in_feedbacks(self):  # просмотр данных в таблице feedbacks
        with self.connection:
            return self.cursor.execute('select * from feedbacks').fetchall()

    def view_data_in_user_questions_to_bot(self):  # просмотр данных в таблице user_questions_to_bot
        with self.connection:
            return self.cursor.execute('select * from user_questions_to_bot').fetchall()

    def add_feedback(self, user_id, username, feedback):  # добавление отзывов в базу данных
        with self.connection:
            try:
                id = sorted(self.cursor.execute('select id from feedbacks').fetchall())[-1][0] + 1
            except IndexError:
                id = 1
            self.cursor.execute('insert into feedbacks values (?, ?, ?, ?)', (id, user_id, username, feedback))
            self.connection.commit()

    def get_feedback(self, user_id):  # получение отзыва пользователя из базы данных
        with self.connection:
            return self.cursor.execute('select feedback from feedbacks where user_id = ?', (user_id,)).fetchone()[0]

    def change_feedback(self, user_id, feedback):  # изменение отзыва пользователя
        with self.connection:
            self.cursor.execute('update feedbacks set feedback = ? where user_id = ?', (feedback, user_id))
            self.connection.commit()

    def add_user_question_to_bot(self, user_id, username, question, answer_bot=None):  # добавление вопросов от пользователей к боту в базу данных
        with self.connection:
            try:
                id = sorted(self.cursor.execute('select id from user_questions_to_bot').fetchall())[-1][0] + 1
            except IndexError:
                id = 1
            self.cursor.execute('insert into user_questions_to_bot values (?, ?, ?, ?, ?)', (id, user_id, username, question, answer_bot))
            self.connection.commit()

    def add_data_to_support(self, questions, answer):  # добавление данных в таблицу support
        with self.connection:
            try:
                id = sorted(self.cursor.execute('select id from support').fetchall())[-1][0] + 1
            except IndexError:
                id = 1
            self.cursor.execute('insert into support values (?, ?, ?)', (id, questions, answer))
            self.connection.commit()

    def delete_data_from_support(self, id):  # удаление данных из таблицы support
        with self.connection:
            self.cursor.execute('delete from support where id = ?', (id,))
            self.connection.commit()

    def change_id_in_support(self, new_data, id):  # изменение колонки id в таблице support
        with self.connection:
            self.cursor.execute('update support set id = ? where id = ?', (new_data, id))
            self.connection.commit()

    def change_questions_in_support(self, new_data, id):  # изменение колонки questions в таблице support
        with self.connection:
            self.cursor.execute('update support set questions = ? where id = ?', (new_data, id))
            self.connection.commit()

    def change_answer_in_support(self, new_data, id):  # изменение колонки answer в таблице support
        with self.connection:
            self.cursor.execute('update support set answer = ? where id = ?', (new_data, id))
            self.connection.commit()

    def add_appeal_to_operator(self, user_id, username):  # добавление данных пользователей, которые вызвали оператора, в базу данных
        with self.connection:
            try:
                id = sorted(self.cursor.execute('select id from appeals_to_operators').fetchall())[-1][0] + 1
            except IndexError:
                id = 1
            self.cursor.execute('insert into appeals_to_operators values (?, ?, ?)', (id, user_id, username))
            self.connection.commit()
            return id

    def get_user_id_from_appeals_to_operators(self, id):  # получение id пользователя из базы данных appeals_to_operators
        with self.connection:
            return self.cursor.execute('select user_id from appeals_to_operators where id = ?', (id,)).fetchone()[0]
