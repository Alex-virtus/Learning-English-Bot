import json

from app.database.db import SessionLocal
from app.database.models import Users


def get_or_create_user(telegram_id: int):
    with SessionLocal() as session:
        user = session.query(Users).filter_by(telegram_id=telegram_id).first()
        if not user:
            print(f"👤 Создание нового пользователя: {telegram_id}")
            user = Users(
                telegram_id=telegram_id,
                study_progress=json.dumps({"queue": [], "index": 0, "total": 0})
            )
            session.add(user)
            session.commit()
            session.refresh(user)
            print(f"✅ Пользователь создан id: {user.user_id}")
        return user
