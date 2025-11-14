import json
import random

from app.database.db import SessionLocal
from app.database.models import Users, Users_words, Words


def build_queue_for_user(session, user_id):
    queue = []

    user_links = session.query(Users_words).filter_by(user_id=user_id).all()
    user_word_ids = [l.word_id for l in user_links]

    common_words = session.query(Words).filter(Words.common_word == True).all()
    common_word_ids = [w.word_id for w in common_words]

    queue.extend([("user", wid) for wid in user_word_ids])
    queue.extend([("common", wid) for wid in common_word_ids])
    random.shuffle(queue)
    return queue


def reset_user_study_session(user: Users):
    user.study_progress = json.dumps({"queue": [], "index": 0, "total": 0})
    with SessionLocal() as session:
        session.add(user)
        session.commit()


def get_random_study_word(user_tg_id: int):
    with SessionLocal() as session:
        user = session.query(Users).filter_by(telegram_id=user_tg_id).first()
        if not user:
            return None, None, None, None, "0 / 0"

        progress = json.loads(user.study_progress or '{"queue":[],"index":0,"total":0}')

        if not progress["queue"]:
            queue = build_queue_for_user(session, user.user_id)
            progress = {"queue": queue, "index": 0, "total": len(queue)}
            user.study_progress = json.dumps(progress)
            session.add(user)
            session.commit()

        idx = progress["index"]
        if idx >= progress["total"]:
            reset_user_study_session(user)
            return None, None, None, None, f"{progress['total']} / {progress['total']}"

        source, target_id = progress["queue"][idx]

        if source == "user":
            target = (
                session.query(Words)
                .join(Users_words)
                .filter(
                    Users_words.user_id == user.user_id,
                    Words.word_id == target_id
                )
                .first()
            )
        else:
            target = session.query(Words).filter_by(word_id=target_id).first()

        if not target:
            progress["index"] += 1
            user.study_progress = json.dumps(progress)
            session.add(user)
            session.commit()
            return get_random_study_word(user_tg_id)

        distractors = session.query(Words.eng_word).filter(
            Words.word_id != target.word_id
        ).all()
        distractors = [d[0] for d in distractors]
        distractors = random.sample(distractors, min(3, len(distractors)))

        options = [target.eng_word] + distractors
        random.shuffle(options)

        progress["index"] += 1
        user.study_progress = json.dumps(progress)
        session.add(user)
        session.commit()

        return target, options, source, target.word_id, f"{progress['index']} / {progress['total']}"
