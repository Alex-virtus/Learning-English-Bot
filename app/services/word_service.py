from app.database.db import SessionLocal
from app.database.models import Users_words, Words


def add_user_word(user_id: int, eng_word: str, rus_word: str):
    with SessionLocal() as session:
        word = session.query(Words).filter_by(eng_word=eng_word.lower()).first()
        if not word:
            word = Words(
                eng_word=eng_word.lower(),
                rus_word=rus_word.lower(),
                common_word=False
            )
            session.add(word)
            session.commit()
            session.refresh(word)

        link = session.query(Users_words).filter_by(
            user_id=user_id, word_id=word.word_id
        ).first()
        if link:
            return False, "Такое слово уже есть в словаре"

        session.add(Users_words(user_id=user_id, word_id=word.word_id))
        session.commit()
        return True, "Слово успешно добавлено"


def get_user_words(user_id: int):
    with SessionLocal() as session:
        links = session.query(Users_words).filter_by(user_id=user_id).all()
        return [
            session.query(Words).filter_by(word_id=l.word_id).first() for l in links
        ]


def delete_user_word(user_id: int, eng_word: str):
    with SessionLocal() as session:
        word = session.query(Words).filter_by(eng_word=eng_word.lower()).first()
        if not word:
            return False
        deleted = session.query(Users_words).filter_by(
            user_id=user_id, word_id=word.word_id
        ).delete()
        session.commit()
        return deleted > 0


def delete_all_user_words(user_id: int):
    with SessionLocal() as session:
        deleted = session.query(Users_words).filter_by(user_id=user_id).delete()
        session.commit()
        return deleted
