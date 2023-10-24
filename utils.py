import json

def load_json_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

def get_prompt_by_title(filename, title, capital):
    data = load_json_file(filename)
    prompt_entry = data.get("prompt")

    if prompt_entry and prompt_entry.get("titre") == title:
        text = prompt_entry.get("texte")
        return text.replace('$capitale', capital)
    else:
        return None

def extract_hint_from_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            hint = data.get("hint", "")
            return hint
    except FileNotFoundError:
        print(f"Le fichier {file_path} n'a pas été trouvé.")
        return None
    except json.JSONDecodeError:
        print(f"Erreur de décodage JSON dans le fichier {file_path}.")
        return None

def parse_strings_to_list(text):
    strings = text.split('\n\n')
    strings = [string.strip() for string in strings]
    return strings

def extract_hint(hint_list):
    tab = []
    for indice in hint_list[1:]:
        description = indice.split(': ')[1]
        tab.append(description)
    return tab