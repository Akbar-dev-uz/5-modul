from collections import defaultdict

import psycopg2


class DataFetcher:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname='quizdb',
            user='postgres',
            password='1234',
            host='localhost',
            port='5432'
        )

    def execute(self, query, params=None):
        with self.conn as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                try:
                    return cursor.fetchall()
                except psycopg2.ProgrammingError:
                    return None

    def get_ct(self):
        category = self.execute("SELECT name, id FROM category")
        return category

    def get_subct(self, ct_id):
        sub_category = self.execute(
            "SELECT s.name, s.id FROM subcategory s JOIN category c ON s.category_id = c.id WHERE s.category_id = %s",
            [ct_id])
        return sub_category

    def get_quiz(self, ct_id, sub_id):
        quiz = self.execute(
            """SELECT q.text, q.id
        FROM quiz q
        JOIN subcategory s ON q.subcategory_id = s.id
        JOIN category c ON s.category_id = c.id
        WHERE s.id = %s AND c.id = %s""", [sub_id, ct_id])
        return quiz

    def get_options(self, ct_id, sub_id, quiz_id):
        my_options = self.execute("""
            SELECT s.name, q.id, o.text, o.is_correct FROM option o
            JOIN quiz q ON q.id = o.quiz_id 
            JOIN subcategory s ON q.subcategory_id = s.id
            """)
        my_dict = defaultdict(list)
        for key, quiz_id, var, is_c in my_options:
            my_dict[key].append((quiz_id, var, is_c))
        return dict(my_dict)

    def get_quiz_id(self, text):
        id = self.execute("SELECT id FROM quiz WHERE text = %s", (text,))
        return id


fetch = DataFetcher()
print(fetch.get_quiz_id('Kuchning SI birligi nima?'))
