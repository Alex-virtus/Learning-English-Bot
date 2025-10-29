from app.database.db import get_session
from app.database.models import UserWord


def add_user_word(user_id: int, english: str, russian: str):
    session = get_session()
    try:
        word = (
            session.query(UserWord)
            .filter_by(user_id=user_id, english=english.lower())
            .first()
        )
        if word:
            return False, "Такое слово уже есть в словаре"

        new_word = UserWord(
            user_id=user_id,
            english=english.lower(),
            russian=russian.lower(),
        )
        session.add(new_word)
        session.commit()
        return True, "Слово успешно добавлено"

    except Exception as e:
        session.rollback()
        print(f"❌ Ошибка добавления слова (id={user_id}): {e}")
        return False, f"Ошибка при добавлении слова: {e}"
    finally:
        session.close()


def delete_user_word(user_id: int, english: str):
    session = get_session()
    try:
        count = (
            session.query(UserWord)
            .filter_by(user_id=user_id, english=english.lower())
            .delete()
        )
        session.commit()
        return count > 0

    except Exception as e:
        print(f"❌ Ошибка удаления слова (id={user_id}): {e}")
        return False
    finally:
        session.close()


def get_user_words(user_id: int):
    session = get_session()
    try:
        return session.query(UserWord).filter_by(user_id=user_id).all()
    except Exception as e:
        print(f"❌ Ошибка получения слов пользователя {user_id}: {e}")
        return []
    finally:
        session.close()


def delete_all_user_words(user_id: int):
    session = get_session()
    deleted = (
        session.query(UserWord)
        .filter(UserWord.user_id == user_id)
        .delete()
    )
    session.commit()
    session.close()
    return deleted
