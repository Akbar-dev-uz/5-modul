import psycopg2


class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="test_bot_db",
            user="postgres",
            password="1234",
            host="localhost",
            port="5432"
        )
        self.curr = self.conn.cursor()
        self.create()

    def create(self):
        self.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id SERIAL PRIMARY KEY,
            username VARCHAR(255),
            first_name VARCHAR(255) NOT NULL,
            last_name VARCHAR(255),
            chat_id BIGINT NOT NULL UNIQUE,
            user_id BIGINT NOT NULL UNIQUE,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );""")

    def execute(self, query, params=None):
        with self.conn:
            self.curr.execute(query, params)
        return self.curr

    def insert_users(self, username, first_name, last_name, chat_id, user_id):
        with self.conn:
            try:
                self.curr.execute("""
                INSERT INTO users (username, first_name, last_name, chat_id, user_id) VALUES (%s,%s,%s,%s,%s)""",
                                  (username, first_name, last_name, chat_id, user_id))
            except psycopg2.errors.UniqueViolation:
                print("User already exists")
