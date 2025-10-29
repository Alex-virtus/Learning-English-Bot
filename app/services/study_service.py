import random
from typing import Optional, Tuple, List

from app.database.db import get_session
from app.database.models import Word, UserWord, User

active_sessions: dict[int, dict] = {}


def build_queue_for_user(session, user_db_id: int) -> List[tuple]:
    queue: List[tuple] = []
    for w in session.query(Word).all():
        queue.append(("base", w.id))
    for w in session.query(UserWord).filter_by(user_id=user_db_id).all():
        queue.append(("user", w.id))
    return queue


def reset_user_study_session(user_id: int):
    active_sessions.pop(user_id, None)


def get_random_study_word(
        user_tg_id: int,
) -> Tuple[Optional[object], Optional[list],
Optional[str], Optional[int], str]:
    session = get_session()
    try:
        user = session.query(User).filter_by(telegram_id=user_tg_id).first()
        if not user:
            print(f"⚠️ Пользователь telegram_id={user_tg_id} не найден.")
            return None, None, None, None, "0 / 0"

        u_id = user.id
        u_sess = active_sessions.get(user_tg_id)

        if not u_sess:
            queue = build_queue_for_user(session, u_id)
            active_sessions[user_tg_id] = {
                "queue": queue, "index": 0, "total": len(queue)
            }
            u_sess = active_sessions[user_tg_id]

        queue = u_sess["queue"]
        idx = u_sess["index"]

        if not queue or idx >= len(queue):
            reset_user_study_session(user_tg_id)
            total = len(queue)
            return None, None, None, None, f"{total} / {total}"

        source, target_id = queue[idx]
        u_sess["index"] += 1

        target = (
            session.query(Word).filter_by(id=target_id).first()
            if source == "base"
            else session.query(UserWord).filter_by(id=target_id).first()
        )

        if not target:
            return get_random_study_word(user_tg_id)

        base_all = session.query(Word).all()
        user_all = session.query(UserWord).filter_by(user_id=u_id).all()
        all_words = base_all + user_all

        others = [w.english for w in all_words if w.english != target.english]
        distractors = random.sample(others, min(3, len(others))) if others else []
        options = [target.english] + distractors
        random.shuffle(options)

        progress = f"{idx + 1} / {u_sess['total']}"
        return target, options, source, target.id, progress

    except Exception as e:
        print(f"Ошибка study_serv.get_random_study_word({user_tg_id}): {e}")
        return None, None, None, None, "0 / 0"
    finally:
        session.close()
