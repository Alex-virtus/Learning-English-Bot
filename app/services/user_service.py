from app.database.db import get_session
from app.database.models import User


def get_or_create_user(telegram_id: int):
    session = get_session()
    try:
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        if not user:
            print(f"👤 Создание нового пользователя: {telegram_id}")
            user = User(telegram_id=telegram_id)
            session.add(user)
            session.commit()
            session.refresh(user)
            print(f"✅ Пользователь создан id: {user.id}")

        return user

    except Exception as e:
        print(f"❌ Ошибка в user_service для id {telegram_id}: {e}")
        session.rollback()
        return None
    finally:
        session.close()
