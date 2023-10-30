import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from continent import ContinentView
import asyncio
import utils
import generate_img
import json
import generate_enigma
from discord import Embed, Button, ButtonStyle, ActionRow
import game

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True

load_dotenv()
intents = discord.Intents.all()
token = os.environ.get("TOKEN")
api_key_openai = os.environ.get("APIKEY_OPENAI")

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is ready!')

class StartButton(discord.ui.Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        guild = interaction.guild
        channel_name = f"neotown-game-{interaction.user.name.lower()}"
        game_channel = discord.utils.get(guild.text_channels, name=channel_name)
        if not game_channel:
            game_channel = await guild.create_text_channel(name=channel_name)
        await game_channel.send(f"Salut {interaction.user.mention}! Démarrons le jeu!")
        await game.game(interaction, game_channel, api_key_openai, bot)

@bot.command(name='stop')
async def stop(ctx):
    if ctx.channel.name.startswith("neotown-game-"):
        loading_message = await ctx.channel.send("Fermeture de votre partie...")
        dots = "."

        for _ in range(3):
            await loading_message.edit(content=f"Fermeture de votre partie{dots}")
            dots = dots + "." if len(dots) < 3 else "."
            await asyncio.sleep(1)

        await ctx.channel.delete()
    else:
        await ctx.send("Ce n'est pas un canal de jeu valide pour l'utilisation de cette commande.")

@bot.command(name='start')
async def start(ctx):
    await info(ctx)
    view = discord.ui.View()
    button = StartButton(label="Commencer une partie", style=discord.ButtonStyle.primary, custom_id="start_game")
    view.add_item(button)
    embed = Embed(title="NeoTown", description="Prêt à commencer le jeu?", color=0x3498db)
    await ctx.send(embed=embed, view=view)

@bot.command(name='info')
async def info(ctx):
    embed = await utils.game_presentation_embed(ctx)
    await ctx.send(embed=embed)

bot.run(token)
