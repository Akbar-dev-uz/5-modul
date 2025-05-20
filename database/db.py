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

    def db_for_game(self):
        self.execute("""
        CREATE TABLE IF NOT EXISTS game(
        id SERIAL PRIMARY KEY,
        username VARCHAR(255),
        user_id BIGINT NOT NULL,
        chat_id BIGINT NOT NULL,
        category VARCHAR(255),
        results VARCHAR(255),
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )""")

    def execute(self, query, params=None):
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(query, params)
                try:
                    return cur.fetchall()
                except psycopg2.ProgrammingError:
                    return None

    def insert_users(self, username, first_name, last_name, chat_id, user_id):
        check = self.execute("SELECT * FROM users WHERE chat_id=%s AND user_id=%s", (chat_id, user_id))
        if not check:
            try:
                self.execute("""
                INSERT INTO users (username, first_name, last_name, chat_id, user_id) VALUES (%s,%s,%s,%s,%s)""",
                             (username, first_name, last_name, chat_id, user_id))
            except psycopg2.errors.UniqueViolation:
                print(f"User {username} already exists")
            else:
                print(f"User {username} successfully registered")

    def insert_games(self, username, chat_id, user_id, category, results):
        inf = (username, user_id, chat_id, category, results)
        try:
            self.execute(
                """INSERT INTO game (username, user_id, chat_id, category, results) VALUES (%s, %s, %s, %s, %s)""",
                inf)
        except psycopg2.errors.UniqueViolation:
            print(f"User {username} already inserted")
        else:
            print(f"User {username} successfully inserted")
