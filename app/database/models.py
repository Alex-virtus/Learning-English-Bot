from sqlalchemy import (Column, Integer, String, Boolean, ForeignKey,
                        BigInteger)
from sqlalchemy.orm import relationship

from app.database.db import Base


class Users(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    study_progress = Column(String, default=None)
    words = relationship('Users_words', back_populates='users')


class Words(Base):
    __tablename__ = 'words'
    word_id = Column(Integer, primary_key=True)
    eng_word = Column(String(40), nullable=False)
    rus_word = Column(String(40), nullable=False)
    common_word = Column(Boolean, nullable=False)
    users = relationship('Users_words', back_populates='words')


class Users_words(Base):
    __tablename__ = 'users_words'
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete="CASCADE"),
                     primary_key=True)
    word_id = Column(Integer, ForeignKey('words.word_id', ondelete="CASCADE"),
                     primary_key=True)
    words = relationship('Words', back_populates='users')
    users = relationship('Users', back_populates='words')
