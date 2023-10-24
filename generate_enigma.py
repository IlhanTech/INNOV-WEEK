import requests
import openai
import json

def get_hint_from_gpt(api_key_openai, prompt):
    openai.api_key = api_key_openai
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    if response:
        return response.choices[0].message['content'].strip()
    else:
        print("Erreur lors de la requête à OpenAI.")
        return None

def parse_response_ia(response):
    if response:
        try:
            parsed_data = json.loads(response)
            isolated_indices = [parsed_data[f"indice {i}"] for i in range(1, len(parsed_data) + 1)]
            return isolated_indices
        except json.JSONDecodeError:
            print("Erreur de décodage JSON : contenu invalide")
            return None
    else:
        print("Réponse vide")
        return None




