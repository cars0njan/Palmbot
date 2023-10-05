import os
import pandas as pd

import discord
from discord import app_commands
from discord.app_commands import Choice
#from discord.ext import commands

import alive
import functions as fx
import text

import requests
from bs4 import BeautifulSoup as BS


intents = discord.Intents.all()
#intents.message_content = True

#client = commands.Bot(command_prefix='=',intents=intents)

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

    await tree.sync()

    stats_csv = pd.read_csv('./data/stats.csv')
    stats_csv.Guilds[0] = len(client.guilds)

    users = 0
    for guild in client.guilds:
        users = users + guild.member_count
    stats_csv.Users[0] = users
    
    stats_csv.to_csv("./data/stats.csv", index=False)

@client.event
async def on_message(msg):
    if msg.author == client.user:
        return

    if msg.content.startswith('$Palmbot$'):
        await msg.channel.send('Hello!')

#####

@tree.command(description = "check if bot is online | bot latency")
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
        file_path = './data/feedback.csv'
        i = fx.read_tail_index(file_path)
        index = int(i) + 1

        if len(content) > 2000:
            await interaction.response.send_message('error - long content: string input for `content` exceed 2000 characters', ephemeral=True)
            return
        if file != None:
            if file.size > 10485760:
                await interaction.response.send_message('error - file size too large: file input for `file` exceed 10MB', ephemeral=True)
                return
                
        d_index = f'"{index}"'
        d_type = f'"{type.value}"'
        content = content.replace('"',"'")
        d_content = f'"{content}"'
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
        await interaction.response.send_message('error - unknown error: cannot log your response. Please try later or use `/contact` function', ephemeral=True)
        raise

tree.add_command(feedback)

#####

@tree.command(description = "Contact developer")
async def contact(interaction: discord.Interaction):
    await interaction.response.send_message(text.text['contact'],ephemeral=True)
    fx.stats()

#####

@tree.command(description='see documentation')
async def docs(interaction: discord.Interaction):
    docs_text = text.text['docs']
    await interaction.response.send_message(
    docs_text,
    file = discord.File(r'./Documentation.md'),
    ephemeral = True
    )
    fx.stats()

#####
@app_commands.command(description='Is AP-Calculus today/tomorrow day-1 or day-2?')
@app_commands.describe(tmr='Check for tomorrow')
@app_commands.choices(tmr=[
    Choice(name='True', value=1),
    Choice(name='False', value=0)
],private_response=[
    Choice(name='True', value=1),
    Choice(name='False', value=0)
])
async def ap_cal(
    interaction:discord.Interaction,
    tmr : Choice[int] = 0,
    private_response: Choice[int] = True
):
    current_month = fx.datetime_van().strftime('%b')
    current_day = int(fx.datetime_van().strftime('%d'))
    if tmr != 0:
        tmr_val = tmr.value
    else:
        tmr_val = 0
    if private_response != True:
        private_response_val = bool(private_response.value)
    else:
        private_response_val = True

    r = requests.get('https://whmkwan.wixsite.com/math/ap-calculus')
    text = BS(r.text, features='html.parser').prettify()
    soup = BS(text, 'html.parser')
    
    p_spans = soup.find_all('p')
    h6_spans = soup.find_all('h6')
    
    spans = p_spans + list(set(h6_spans) - set(p_spans))
    #print('__start__')
    target_spans =[]
    
    for span in spans:
        span_text = span.text.strip()
        if span_text.startswith(f'{current_month}. {current_day+ tmr_val} - '):
            target_spans.append(span_text)
    
    if len(target_spans) ==0:
        await interaction.response.send_message('error - no result', ephemeral=True)
        #print('error - no result')
        return
    if len(list(set(target_spans))) > 1:
        await interaction.response.send_message('error - too many results', ephemeral=True)
        #print('error - multiple results')
        return
    await interaction.response.send_message(f'AP-Calculus\n{target_spans[0]}', ephemeral=private_response_val)
    fx.stats()
    #print(target_spans[0])

tree.add_command(ap_cal)

#####
# @tree.command(description = "Owner Only: restart bot")
# @fx.is_owner()
# async def restart(interaction:discord.Interaction):
#     await interaction.response.send_message('restarting bot', ephemeral=True)
#     os.system("python restarter.py")
#     os.system('kill 1 &')

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
#        os.system("python restarter.py")
        os.system('kill 1 &')
    else:
        raise e
