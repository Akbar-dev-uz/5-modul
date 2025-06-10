import psycopg2

from sqlalchemy import create_engine, Column, Integer, String, BIGINT, DateTime, func, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
from os import getenv

load_dotenv()

DB_URL = getenv("DB_URL")

Base = declarative_base()
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String)
    chat_id = Column(BIGINT, unique=True, nullable=False)
    user_id = Column(BIGINT, unique=True, nullable=False)
    created_at = Column(DateTime, default=func.now())

    def __repr__(self):
        fields = ', '.join(
            f"{column.name}={getattr(self, column.name)!r}"
            for column in self.__table__.columns
        )
        return f"{self.__class__.__name__}({fields})"

    @classmethod
    def delete_u_id(cls, user_id):
        with SessionLocal() as session:
            obj = session.query(cls).filter(cls.user_id == user_id).first()
            if obj:
                session.delete(obj)
                session.commit()
                return True
        return False


class Game(Base):
    __tablename__ = "game"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    user_id = Column(BIGINT, nullable=False)
    chat_id = Column(BIGINT, nullable=False)
    category = Column(String)
    results = Column(String)
    created_at = Column(DateTime, default=func.now())

    def __repr__(self):
        fields = ', '.join(
            f"{column.name}={getattr(self, column.name)!r}"
            for column in self.__table__.columns
        )
        return f"{self.__class__.__name__}({fields})"

    @classmethod
    def delete_u_id(cls, user_id):
        with SessionLocal() as session:
            obj = session.query(cls).filter(cls.user_id == user_id).first()
            if obj:
                session.delete(obj)
                session.commit()
                return True
        return False


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

    @staticmethod
    def save_all(instances):
        with SessionLocal() as session:
            session.add_all(instances)
            session.commit()

    @classmethod
    def delete_u_id(cls, user_id):
        with SessionLocal() as session:
            obj = session.query(cls).filter(cls.user_id == user_id).first()
            if obj:
                session.delete(obj)
                session.commit()
                return True
        return False

    @classmethod
    def get_by_u_id(cls, user_id):
        with SessionLocal() as session:
            return session.query(cls).filter(cls.user_id == user_id).first()


class Database:
    @staticmethod
    def execute(query, params=None, fetch=True):
        try:
            with engine.begin() as conn:
                result = conn.execute(text(query), params or {})
                if fetch:
                    return result.fetchall()
        except Exception as e:
            print(f"❗ Error executing query: {e}")
        return None

    @staticmethod
    def check_user(user_id):
        with SessionLocal() as session:
            exists = session.query(User).filter_by(user_id=user_id).first()
            if exists:
                return True
            return False

    @staticmethod
    def check_user_mlt(user_id):
        with SessionLocal() as session:
            exists = session.query(UsersMlt).filter_by(user_id=user_id).first()
            if exists:
                return True
            return False

    @staticmethod
    def save(instance):
        with SessionLocal() as session:
            try:
                session.add(instance)
                session.commit()
            except IntegrityError:
                session.rollback()
                print(f"User {instance.username} already inserted")
            except Exception as e:
                session.rollback()
                print(f"Error saving {instance}: {e}")
            else:
                print(f"User {instance.username} successfully inserted")

    @staticmethod
    def get_lang(user_id):
        with SessionLocal() as session:
            res = session.query(UsersMlt.lang).filter_by(user_id=user_id).first()
        return res[0] if res else None


db = Database()
