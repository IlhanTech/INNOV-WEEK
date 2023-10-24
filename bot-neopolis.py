import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from continent import ContinentView
import asyncio
import utils

load_dotenv()
intents = discord.Intents.all()
token = os.environ.get("TOKEN")
api_key_openai = os.environ.get("APIKEY_OPENAI")

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command(name='start')
async def game(ctx):
    view = ContinentView(api_key_openai)
    message = await ctx.send("Sélectionnez un continent pour commencer le jeu.", view=view)

    await view.selection_done.wait()

    hint = view.hint
    if hint:
        hintab = utils.parse_strings_to_list(hint)
        hints = utils.extract_hint(hintab)
        print(hintab)
        await ctx.send(f"Voici votre premier indice : {' '.join(hints[0])}")
        await ctx.send(f"Voici votre deuxième indice : {' '.join(hints[1])}")
        await ctx.send(f"Voici votre troisième indice : {' '.join(hints[2])}")
    else:
        await ctx.send("Aucun indice trouvé.")


bot.run(token)
