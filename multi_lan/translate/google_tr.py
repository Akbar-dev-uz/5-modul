import json
from os import path
from database.db import Database

BASE_DIR = path.dirname(path.dirname(__file__))


def get_text(user_id, full_name):
    db_mlt = Database()
    lang = db_mlt.get_lang(user_id)
    with open(f"{BASE_DIR}/{lang}/data.json", 'r', encoding='utf-8') as file:
        data = json.load(file)
        text = data["start"].format(full_name=full_name)
        return text

