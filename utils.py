import json
import re

def load_json_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

def get_prompt_by_title(filename, title, continent):
    data = load_json_file(filename)
    prompt_entry = data.get("prompt")

    if prompt_entry and prompt_entry.get("titre") == title:
        text = prompt_entry.get("texte")
        replaced_text = text.replace('$continent', continent)
        print(replaced_text)
        return replaced_text
    else:
        return None

def parse_json(data: str) -> dict:
    parsed_data = json.loads(data)
    city = parsed_data["city"]
    popularity = parsed_data["popularity"]
    dalle_prompt = None
    indice_1 = None
    indice_2 = None

    for clue in parsed_data["clues"]:
        if clue["type"] == "DALL·E Image Prompt":
            dalle_prompt = clue["content"]
        elif clue["type"] == "Indice 1":
            indice_1 = clue["content"]
        elif clue["type"] == "Indice 2":
            indice_2 = clue["content"]

    return {
        "city": city,
        "popularity": popularity,
        "dalle_prompt": dalle_prompt,
        "indice_1": indice_1,
        "indice_2": indice_2
    }