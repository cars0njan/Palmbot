import os

import discord
from discord import app_commands
from discord.ext import commands

import alive

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='=',intents=intents)



@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.tree.sync()


@client.event
async def on_message(msg):
    if msg.author == client.user:
        return

    if msg.content.startswith('$Palmbot$'):
        await msg.channel.send('Hello!')

@client.tree.command(name='ping', description='Show bot ping and check if bot is online.')
async def ping(interaction: discord.Interaction):
    latency = round(client.latency * 1000)
    await interaction.response.send_message(f'**{latency}** ms. Bot is online.',ephemeral=True)

try:
    token = os.getenv("TOKEN") or ""
    if token == "":
        raise Exception("Token missing")
    alive.alive()
    client.run(token)

except discord.HTTPException as e:
    if e.status == 429:
        print(e)
        os.system("python restart.py")
        os.system('kill 1')
    else:
        raise e
