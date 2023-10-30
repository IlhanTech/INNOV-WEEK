import json
import re
import asyncio
import discord

def load_json_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

def get_prompt_by_title(filename, title, continent):
    data = load_json_file(filename)
    prompt_entry = data.get("prompt1")

    if prompt_entry and prompt_entry.get("titre") == title:
        text = prompt_entry.get("texte")
        replaced_text = text.replace('$continent', continent)
        print(replaced_text)
        return replaced_text
    else:
        return None

def get_prompt_by_title_city(filename, title, ville):
    data = load_json_file(filename)
    prompt_entry = data.get("prompt2")

    if prompt_entry and prompt_entry.get("titre") == title:
        text = prompt_entry.get("texte")
        replaced_text = text.replace('$ville', ville)
        print(replaced_text)
        return replaced_text
    else:
        return None


def parse_json(data: str) -> dict:
    parsed_data = json.loads(data)
    agent_data = parsed_data["agent"]
    city = agent_data["city"]
    continent = agent_data["continent"]
    country = agent_data.get("country")
    dalle_prompt = None
    if agent_data["clues"]:
        dalle_prompt = agent_data["clues"][0]["content"]
    return {
        "city": city,
        "continent": continent,
        "country": country,
        "dalle_prompt": dalle_prompt,
    }

async def display_loading_animation(channel):
    loading_message = await channel.send("Chargement de votre partie...")
    dots = "."

    for _ in range(5):
        await loading_message.edit(content=f"Chargement de votre partie{dots}")
        dots = dots + "." if len(dots) < 3 else "."
        await asyncio.sleep(1)
    await loading_message.edit(content="Votre partie est prête!")

async def game_presentation_embed(ctx):
    with open('assets/img/LOGO_NEOTOWN.png', 'rb') as f:
        picture = await ctx.send(file=discord.File(f, 'LOGO_NEOTOWN.png'))

    img_url = picture.attachments[0].url
    embed = discord.Embed(
        title="🌍 NeoTown - Devinez la Ville 🌍",
        description=("Bienvenue à NeoTown, le jeu où vous devinez des villes du monde entier!"
                     "\n\n"
                     "🔍 Votre mission est d'interroger un agent intelligent pour deviner le nom de la ville sur laquelle il est spécialisé."
                     "\n"
                     "🚫 L'agent donnera des indices, mais ne mentionnera jamais directement le nom de la ville!"
                     "\n\n"
                     "✨ Alors, êtes-vous prêt à relever le défi et à devenir le maître de la géographie mondiale? ✨"),
        color=0x3498db
    )
    embed.set_footer(text="Lancez le jeu en sélectionnant un continent ci-dessous!")
    embed.set_thumbnail(url=img_url)
    return embed
