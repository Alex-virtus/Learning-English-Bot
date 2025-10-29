import os
from urllib.parse import quote_plus

from dotenv import load_dotenv

load_dotenv()

TG_TOKEN = os.getenv("TG_TOKEN")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD"))
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DSN = (f"postgresql+psycopg2://"
       f"{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

if not TG_TOKEN:
    print("⚠️  ВНИМАНИЕ: TG_TOKEN не установлен.")
if not all([DB_USER, DB_PASSWORD, DB_NAME]):
    print("⚠️  ВНИМАНИЕ: Не все настройки БД установлены, проверьте .env.")
