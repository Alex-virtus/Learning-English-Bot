from app.database.db import Base, engine, SessionLocal
from app.database.models import Words
import json

def init_db():
    print("⚙️ Инициализация базы данных...")
    Base.metadata.create_all(bind=engine)
    seed_default_words()

def seed_default_words():
    default_words = [
        ('blue', 'синий'),
        ('he', 'он'),
        ('I', 'я'),
        ('friend', 'друг'),
        ('white', 'белый'),
        ('red', 'красный'),
        ('see', 'видеть'),
        ('go', 'идти'),
        ('green', 'зелёный'),
        ('family', 'семья'),
        ('she', 'она'),
        ('you', 'ты'),
        ('house', 'дом'),
        ('black', 'чёрный'),
        ('we', 'мы')
    ]

    with SessionLocal() as session:
        count = session.query(Words).filter_by(common_word=True).count()
        if count == 0:
            print('🔄 Добавление начальных слов в общий словарь...')
            for eng, rus in default_words:
                session.add(Words(eng_word=eng.lower(),
                                  rus_word=rus.lower(), common_word=True))
            session.commit()
            print(f'✅ В БД добавлено {len(default_words)} слов.')
        else:
            print(f'ℹ️ В БД уже есть {count} слов.')
