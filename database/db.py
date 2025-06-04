import psycopg2

from sqlalchemy import create_engine, Column, Integer, String, BIGINT, DateTime, func
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
from os import getenv

load_dotenv()

DB_URL = getenv("DB_URL")
engine = create_engine(DB_URL)
Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)


class UsersMlt(Base):
    __tablename__ = "users_mlt_lan"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String)
    chat_id = Column(BIGINT, unique=True)
    user_id = Column(BIGINT, unique=True)
    lang = Column(String(2))
    phone_number = Column(String(14))
    email = Column(String)
    created_at = Column(DateTime, default=func.now())

    def __repr__(self):
        fields = ', '.join(
            f"{column.name}={getattr(self, column.name)!r}"
            for column in self.__table__.columns
        )
        return f"{self.__class__.__name__}({fields})"

    def save(self):
        with SessionLocal() as session:
            session.add(self)
            session.commit()

    @staticmethod
    def save_all(instances):
        with SessionLocal() as session:
            session.add_all(instances)
            session.commit()

    @classmethod
    def delete_cls(cls, id_):
        with SessionLocal() as session:
            obj = session.query(cls).filter(cls.id == id_).first()
            if obj:
                session.delete(obj)
                session.commit()
                return True
        return False

    @classmethod
    def get_by_id(cls, id_):
        with SessionLocal() as session:
            return session.query(cls).filter(cls.id == id_).first()


# Base.metadata.create_all(engine)


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

    def check_user(self, user_id):
        check = self.execute("SELECT * FROM users WHERE user_id=%s", (user_id,))
        if check:
            return True
        return False

    def insert_users(self, username, first_name, last_name, chat_id, user_id):
        check = self.check_user(user_id)
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
