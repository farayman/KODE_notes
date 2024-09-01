import json
import requests
from typing import List
from fastapi import HTTPException

DATA_FILE = 'data.json'
YANDEX_SPELLER_URL = "https://speller.yandex.net/services/spellservice.json/checkText"

def read_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {'users': [], "notes": []}
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail="Error reading JSON file: " + str(e))
def write_data(data):
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f)
    except IOError as e:
        raise HTTPException(status_code=500, detail="Error writing JSON file: " + str(e))

def check_spelling(text: str) -> List[dict]:
    try:
        url = "https://speller.yandex.net/services/spellservice.json/checkText"
        params = {"text": text}
        response = requests.get(url, params=params)

        if response.status_code == 200:
            corrections = response.json()
            for correction in corrections:
                word = correction['word']
                s = correction['s']
                if s:
                    text = text.replace(word, s[0])
        return text
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail="Error checking spelling")


