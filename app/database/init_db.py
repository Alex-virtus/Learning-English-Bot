from app.database.db import Base, engine, get_session
from app.database.models import Word

DEFAULT_WORDS = [
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


def init_db():
    Base.metadata.create_all(engine)
    session = get_session()
    try:
        existing_words_count = session.query(Word).count()
        if existing_words_count == 0:
            print('🔄 Добавление начальных слов в базу данных...')
            for english_word, russian_translation in DEFAULT_WORDS:
                word = Word(english=english_word, russian=russian_translation)
                session.add(word)

            session.commit()
            print(f'✅ В БД добавлено {len(DEFAULT_WORDS)} общих слов.')
        else:
            print(f'ℹ️ БД уже содержит {existing_words_count} слов.')

        words = session.query(Word).all()
        print('\n📚 ОБЩИЕ СЛОВА В БАЗЕ ДАННЫХ:')
        print('=' * 40)

        for i, word in enumerate(words, start=1):
            print(f'{i:2d}. {word.english:10} - {word.russian}')

        print('=' * 40)

    except Exception as e:
        print(f'❌ Ошибка при инициализации БД: {e}')
        session.rollback()
    finally:
        session.close()
        print('🔒 Соединение с БД закрыто.')
