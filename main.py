import os
import pandas as pd

import discord
from discord import app_commands
from discord.app_commands import Choice
#from discord.ext import commands

import alive
import functions as fx


intents = discord.Intents.all()
#intents.message_content = True

#client = commands.Bot(command_prefix='=',intents=intents)

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

    await tree.sync()

    stats_csv = pd.read_csv('./stats.csv')
    stats_csv.Guilds[0] = len(client.guilds)

    users = 0
    for guild in client.guilds:
        users = users + guild.member_count
    stats_csv.Users[0] = users
    
    stats_csv.to_csv("./stats.csv", index=False)

@client.event
async def on_message(msg):
    if msg.author == client.user:
        return

    if msg.content.startswith('$Palmbot$'):
        await msg.channel.send('Hello!')

#####

@tree.command(description = "Show bot ping and check if bot is online.")
async def ping(interaction: discord.Interaction):
    latency = round(client.latency * 1000)
    await interaction.response.send_message(f'**{latency}** ms. Bot is online.',ephemeral=True)
    fx.stats()

#####

@app_commands.command(description="suggest new functions or report bugs")
@app_commands.describe(file='attach screenshots or code files. DO NOT include personal info as the log is unecrypted.')
@app_commands.choices(type=[
    Choice(name='Report bug', value='Bug'),
    Choice(name='Suggest functions', value='Functions'),
    Choice(name='Others', value='Other'),
])
async def feedback(
    interaction: discord.Interaction,
    type: Choice[str],
    content: str,
    file: discord.Attachment = None 
):
    try:
        file_path = './feedback.csv'
        i = fx.read_tail_index(file_path)
        index = int(i) + 1

        if len(content) > 2000:
            await interaction.response.send_message('error: maximum 2000 characters for field "content"', ephemeral=True)
            return
        if file != None:
            if file.size > 10485760:
                await interaction.response.send_message('error: maximum file of 10MB for field "file"', ephemeral=True)
                return
                
        d_index = f'"{index}"'
        d_type = f'"{type.value}"'
        d_content = f'"{content.replace('"',"'")}"'
        d_resolved = f'"FALSE"'
        
        if file == None:
            d_file = f'"FALSE"'
            data = f'{d_index},{d_type},{d_content}, {d_file},{d_resolved}'
        else:
            d_file = f'"TRUE"'
            data = f'{d_index},{d_type},{d_content}, {d_file},{d_resolved}'
            filetype= file.content_type.split('/')[-1]
            await file.save(f'./feedback_files/feedback_file_{index}.{filetype}')
        
        fx.csv_append(file_path, data)
        
        await interaction.response.send_message('Your response has been sent. Thank you.', ephemeral=True)
        fx.stats()
    except:
        await interaction.response.send_message('Unknown error in logging your response. Please try later or use `contact` function', ephemeral=True)
        raise

tree.add_command(feedback)

#####

@tree.command(description = "Contact developer")
async def contact(interaction: discord.Interaction):
    await interaction.response.send_message(f'To contact the developer, please email `sc.carson.jan@gmail.com`\n\n*To suggest new functions or report bugs, please use the* `feedback` *command instead*',ephemeral=True)

#####



#####
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
