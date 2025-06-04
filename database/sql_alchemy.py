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
