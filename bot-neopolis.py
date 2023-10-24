import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from continent import ContinentView
import asyncio
import utils
import generate_img

load_dotenv()
intents = discord.Intents.all()
token = os.environ.get("TOKEN")
api_key_openai = os.environ.get("APIKEY_OPENAI")

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command(name='play')
async def game(ctx):
    view = ContinentView(api_key_openai)
    message = await ctx.send("Sélectionnez un continent pour commencer le jeu.", view=view)

    await view.selection_done.wait()

    hint = view.hint
    if hint and 'clues' in hint:
        try:
            data = utils.parse_json(hint)
            dalle_prompt = data["dalle_prompt"]
            indice1_content = data["indice_1"]
            indice2_content = data["indice_2"]
            city = data["city"]
            await ctx.send(generate_img.generate_img_dalle(api_key_openai, dalle_prompt))
            await ctx.send(indice1_content)
            await ctx.send(indice2_content)
            await ctx.send(city)
        except ValueError:
            await ctx.send("Il y a eu un problème en extrayant les indices.")
        except KeyError as ke:
            await ctx.send(f"Il y a eu une erreur lors de l'accès à la clé: {ke}")
    else:
        await ctx.send("Aucun indice trouvé.")


bot.run(token)
