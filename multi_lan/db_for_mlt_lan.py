# import psycopg2
# from dotenv import load_dotenv
# from os import getenv
#
# load_dotenv()
#
# DB_URL = getenv("DB_URL")
#
#
# class Database:
#     def __init__(self):
#         self.conn = psycopg2.connect(DB_URL)
#         self.create()
#
#     def create(self):
#         self.execute("""
#         CREATE TABLE IF NOT EXISTS users_mlt_lan(
#             id SERIAL PRIMARY KEY,
#             username VARCHAR(255),
#             first_name VARCHAR(255) NOT NULL,
#             last_name VARCHAR(255),
#             chat_id BIGINT NOT NULL UNIQUE,
#             user_id BIGINT NOT NULL UNIQUE,
#             lang VARCHAR(255) NOT NULL DEFAULT 'ru',
#             created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
#         );""")
#
#     def execute(self, query, params=None):
#         with self.conn:
#             with self.conn.cursor() as cur:
#                 cur.execute(query, params)
#                 try:
#                     return cur.fetchall()
#                 except psycopg2.ProgrammingError:
#                     return None
#
#     def insert_mlt_lan(self, username, first_name, last_name, chat_id, user_id, lang):
#         check = self.execute("SELECT * FROM users_mlt_lan WHERE chat_id=%s AND user_id=%s", (chat_id, user_id))
#         if not check:
#             try:
#                 self.execute("""INSERT INTO users_mlt_lan (username, first_name, last_name, chat_id, user_id, lang)
#                  VALUES (%s,%s,%s,%s,%s,%s)""",
#                              (username, first_name, last_name, chat_id, user_id, lang))
#             except psycopg2.errors.UniqueViolation:
#                 print(f"User {username} already exists")
#             else:
#                 print(f"User {username} successfully registered")
#
#     def check_mlt_user(self, user_id):
#         user = self.execute("SELECT * FROM users_mlt_lan WHERE user_id = %s", (user_id,))
#         if user:
#             return True
#         else:
#             return False
#
