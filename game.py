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

async def check_win_condition(game_channel, raw_answer):
    if '[FIND]' in raw_answer:
        embed = discord.Embed(
            title="Félicitations !",
            description="Vous avez trouvé la ville ! 🎉",
            color=0x2ecc71
        )
        await game_channel.send(embed=embed)
        return True
    return False

async def game(interaction: discord.Interaction, game_channel: discord.TextChannel, api_key_openai, bot):
    num_questions = 4
    question = "questions"
    view = ContinentView(api_key_openai)
    await game_channel.send(embed=Embed(title="NeoTown", description="Sélectionnez un continent pour commencer le jeu.", color=0x3498db), view=view)
    await view.selection_done.wait()
    hint = view.hint
    if hint and 'clues' in hint:
        try:
            data = utils.parse_json(hint)
            dalle_prompt = data["dalle_prompt"]
            city = data["city"]
            country = data["country"]
            if city:
                city = city.lower()
            img_url = generate_img.generate_img_dalle(api_key_openai, dalle_prompt)
            await game_channel.send(embed=Embed(title="Indice", description="Voici une image pour vous aider à deviner la ville:", color=0xf39c12).set_image(url=img_url))
            for _ in range(num_questions, 0, -1):
                if num_questions == 1:
                    await game_channel.send(embed=Embed(title="Indice Final", description=f"Voilà un indice supplémentaire : le pays dans lequel se trouve la ville est {country}", color=0xe74c3c))
                await game_channel.send(embed=Embed(title="NeoTown", description=f"Vous avez maintenant le droit à {num_questions} {question} afin d'identifier la ville !", color=0x2ecc71))
                def check(m):
                    return m.author == interaction.user and m.channel == game_channel
                user_response = await bot.wait_for('message', check=check)
                response_prompt = utils.get_prompt_by_title_city("assets/json/prompt.json", "AgentDevinetteVille", city)
                response_prompt = response_prompt.replace('"question": ""', f'"question": "{user_response.content}"')
                raw_answer = generate_enigma.get_hint_from_gpt(api_key_openai, response_prompt)
                if await check_win_condition(game_channel, raw_answer):
                    break
                await game_channel.send(embed=Embed(title="Réponse", description=f"{raw_answer}", color=0xf39c12))
                num_questions -= 1
                question = "question" if num_questions == 1 else "questions"
        except Exception as e:
            print(f"Une erreur est survenue : {e}")
