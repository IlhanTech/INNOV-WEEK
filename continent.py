import discord
import json
import random
import generate_enigma
import utils
import asyncio

class ContinentView(discord.ui.View):
    def __init__(self, api_key_openai):
        super().__init__()
        self.api_key_openai = api_key_openai
        self.hint = None
        self.selection_done = asyncio.Event()

    @discord.ui.select(
        placeholder="Sélectionnez un continent",
        options=[
            discord.SelectOption(label="Afrique", value="Afrique"),
            discord.SelectOption(label="Amérique", value="Amérique"),
            discord.SelectOption(label="Antarctique", value="Antarctique"),
            discord.SelectOption(label="Asie", value="Asie"),
            discord.SelectOption(label="Europe", value="Europe"),
            discord.SelectOption(label="Océanie", value="Océanie")
        ]
    )
    async def select_continent(self, interaction: discord.Interaction, select: discord.ui.Select):
        selected_continent = select.values[0]
        await interaction.response.send_message(f"Vous avez sélectioné : {selected_continent}")
        self.hint = await self.handle_continent_selection(selected_continent)
        self.selection_done.set()

    async def handle_continent_selection(self, continent):
        with open('assets/json/capitale.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        for continent_data in data["monde"]:
            if continent_data["continent"] == continent:
                capitales = []
                if "pays" in continent_data:
                    for pays in continent_data["pays"]:
                        if "capitale" in pays:
                            capitales.append(pays["capitale"])
                elif "stations" in continent_data:
                    for station in continent_data["stations"]:
                        if "localisation" in station:
                            capitales.append(station["localisation"])

                if capitales:
                    capitale_choisie = random.choice(capitales)
                    prompt_text = utils.get_prompt_by_title("assets/json/prompt.json", "prompt1", capitale_choisie)
                    hint = generate_enigma.get_hint_from_gpt(self.api_key_openai, prompt_text)
                    return hint
                else:
                    print(f"Aucune capitale trouvée pour {continent}")
