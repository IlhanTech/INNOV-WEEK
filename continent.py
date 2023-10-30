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
        
        loading_task = asyncio.create_task(self.display_loading_animation(interaction.channel))
        hint_task = asyncio.create_task(self.handle_continent_selection(selected_continent))

        self.hint = await hint_task
        await loading_task  # Attend que l'animation de chargement soit terminée
        self.selection_done.set()

    async def display_loading_animation(self, channel):
        loading_message = await channel.send("Chargement de votre partie...")
        dots = "."

        for _ in range(5):
            await loading_message.edit(content=f"Chargement de votre partie{dots}")
            dots = dots + "." if len(dots) < 3 else "."
            await asyncio.sleep(1)
        await loading_message.edit(content="Votre partie est prête!")

    async def handle_continent_selection(self, continent):
        if continent:
            prompt_text = utils.get_prompt_by_title("assets/json/prompt.json", "prompt1", continent)
            for attempt in range(5):
                try:
                    hint = generate_enigma.get_hint_from_gpt(self.api_key_openai, prompt_text)
                    break
                except Exception as e:
                    print(f"Une erreur est survenue lors de la tentative {attempt + 1}: {e}")
                    if attempt == 4:
                        await ctx.send("Désolé, une erreur persiste. Veuillez réessayer plus tard.")
            return hint
        else:
            print(f"Aucun continent trouvée")
