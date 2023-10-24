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
        if continent:
            prompt_text = utils.get_prompt_by_title("assets/json/prompt.json", "prompt1", continent)
            hint = generate_enigma.get_hint_from_gpt(self.api_key_openai, prompt_text)
            return hint
        else:
            print(f"Aucun continent trouvée")
