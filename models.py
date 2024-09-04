import datetime
import os
from atexit import register

from dotenv import load_dotenv
from sqlalchemy import Date, Integer, String, create_engine, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


load_dotenv()

PG_USER = os.getenv('PG_USER')
PG_PASSWORD = os.getenv('PG_PASSWORD')
PG_NAME = os.getenv('PG_NAME')
PG_HOST = os.getenv('PG_HOST')
PG_PORT = os.getenv('PG_PORT')

DSN = f'postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_NAME}'

engine = create_engine(DSN)
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    mail: Mapped[str] = mapped_column(String(128), unique=True)
    password: Mapped[str] = mapped_column(String(72), nullable=False)

    @property
    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'mail': self.mail
        }


class Advertisement(Base):
    __tablename__ = 'advertisement'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(64), nullable=False)
    description: Mapped[str] = mapped_column(String(256), nullable=False)
    create_date: Mapped[datetime.date] = mapped_column(Date, default=datetime.date.today())
    owner: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))
    # owner: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)

    @property
    def json(self):
        return {
            'id': self.id,
            'Заголовок': self.title,
            'Описание': self.description,
            'Дата создания': self.create_date,
            'Владелец': self.owner
        }


Base.metadata.create_all(bind=engine)

register(engine.dispose)
