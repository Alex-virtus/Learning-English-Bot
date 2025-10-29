from sqlalchemy import (Column, Integer, BigInteger, String, ForeignKey,
                        UniqueConstraint)
from sqlalchemy.orm import relationship

from app.database.db import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    words = relationship('UserWord', back_populates='user',
                         cascade='all, delete-orphan')


class Word(Base):
    __tablename__ = 'words'

    id = Column(Integer, primary_key=True)
    english = Column(String, unique=True, nullable=False)
    russian = Column(String, nullable=False)


class UserWord(Base):
    __tablename__ = 'user_words'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    english = Column(String, nullable=False)
    russian = Column(String, nullable=False)
    user = relationship('User', back_populates='words')

    __table_args__ = (UniqueConstraint('user_id', 'english',
                                       name='_user_word_uc'),)
