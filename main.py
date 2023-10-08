import os
import pandas as pd

import discord
from discord import app_commands
from discord.app_commands import Choice
from typing import Literal
from discord.ext import tasks
#from discord.ext import commands

import alive
import functions as fx
import text

import requests
from bs4 import BeautifulSoup as BS
import qrcode


intents = discord.Intents.all()
#intents.message_content = True

#client = commands.Bot(command_prefix='=',intents=intents)

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)



@tasks.loop(minutes=30.0)
async def self_ping():
    requests.head('palmbot.cars0njan.repl.co')
    print(self_ping)

@self_ping.before_loop()
async def before_self_ping():
    await client.wait_until_ready()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

    await tree.sync()

    stats_csv = pd.read_csv('./data/stats.csv')
    stats_csv.Guilds[0] = len(client.guilds)

    users = 0
    for guild in client.guilds:
        users = users + (guild.member_count or 0)
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
@app_commands.command(description='AP-Calculus day for today | your next AP-Cal class')
@app_commands.describe(search_next='Which day are you in? We will show you your next class')

async def ap_cal(
    interaction:discord.Interaction,
    search_next : Literal['Day 1', 'Day 2'] = None
):
    current_month = fx.datetime_van().strftime('%b')
    current_day = int(fx.datetime_van().strftime('%d'))

    r = requests.get('https://whmkwan.wixsite.com/math/ap-calculus')
    text = BS(r.text, features='html.parser').prettify()
    soup = BS(text, 'html.parser')

    p_spans = soup.find_all('p')
    h6_spans = soup.find_all('h6')
    spans = p_spans + list(set(h6_spans) - set(p_spans))

    span_text =[]
    for i in spans:
        i = i.text.strip()
        if (' - Day 1' in i) or (' - Day 2' in i):
            span_text.append(i.lower())

    current_str = f'{current_month}. {current_day} -'.lower()
    def search_today(span_text):
        for i in span_text:
            if i.startswith(current_str):
                return i
    if search_next == None:
        today_str = search_today(span_text) or 'no-class'
        await interaction.response.send_message(f'AP-Calculus\n\nToday: **{today_str.title()}**', ephemeral=True)
        fx.stats()
        return

    month_mapping = {
        'jan.': 1, 'feb.': 2, 'mar.': 3, 'apr.': 4, 'may': 5, 'jun.': 6,
        'jul.': 7, 'aug.': 8, 'sept.': 9, 'oct.': 10, 'nov.': 11, 'dec.': 12
    }

    def sort_key(span_text):
        month, day_description = span_text.split(' - ')
        month, day = month.split(' ')
        return (int(month_mapping[month]), int(day.split('.')[0]), day_description)

    span_text = sorted(span_text, key=sort_key)
    #print(span_text)

    #prefix_str = f'{current_month}. {current_day} -'.lower()
    #print(prefix_str)

    def with_prefix(list):
        for plus in range(0,5):
            for index, i in enumerate(list):
                if i.startswith(f'{current_month}. {current_day+plus} -'.lower()):
                    return index
        return None

    for i in range(with_prefix(span_text),len(span_text)):
        if search_next.lower() in span_text[i]:
            today_str = search_today(span_text) or 'no-class'
            next_str = span_text[i]
            await interaction.response.send_message(f'AP-Calculus\n\nToday: **{today_str.title()}**\nNext: **{next_str.title()}**', ephemeral=True)
            fx.stats()
            return
    await interaction.response.send_message('error - no result', ephemeral=True)
    return

tree.add_command(ap_cal)

#####
@tree.command(description = 'Show school map')
async def map(interaction:discord.Interaction):
    file = discord.File('./data/upload/School_Map.png')
    await interaction.response.send_message(file=file, ephemeral = True)
    fx.stats()

#####
@app_commands.command(description='generate an invite QR code & url')
@app_commands.describe(lifespan='Hours before the code expires. Default to be 48')
@app_commands.describe(temp='Give temporary role')
@app_commands.describe(private='return private response, else broadcast to channel')
async def invite (
    interaction:discord.Interaction, 
    private:Literal['True', 'False'] = 'True',
    lifespan:int = 48, 
    temp: Literal['True', 'False'] = 'False'
    ):
    if not interaction.channel.permissions_for(interaction.user).create_instant_invite:
        await interaction.response.send_message('error - no invite permission', ephemeral=True)
        return
    invite = await interaction.channel.create_invite(
        max_age = lifespan*60*60, 
        temporary = bool(temp), 
        reason = f'invite command triggered by {interaction.user.name}'
    )
    invite_url = invite.url
    invite_qr = qrcode.make(invite_url)
    invite_qr.save("./data/temp/invite_qr.png")
    
    eph = bool(private)

    # with open('./data/temp/inviteqr_file.png','wb') as f:
    #     f.write(invite_qr)
    with open('./data/temp/inviteqr_file.png','rb') as f:
        await interaction.response.send_message(f'{invite_url}', file = discord.File(f), ephemeral = eph)
    os.remove('./data/temp/inviteqr_file.png')
    fx.stats()

tree.add_command(invite)
#####

@app_commands.command(description='make a QR code with a url')
@app_commands.describe(private='return private response, else broadcast to channel')
async def to_qr(
    interaction:discord.Interaction,
    url:str ,
    private:Literal['True', 'False'] = 'True'
    ):
    try:
        invite_qr = qrcode.make(url)
        invite_qr.save("./data/temp/to_qr_qr.png")
    except:
        await interaction.response.send_message('error - invalid url', ephemeral=True)
        raise
        return
        
    
    eph = bool(private)

    # with open('./data/temp/to_qr_qr.png','wb') as f:
    #     f.write(invite_qr)
    with open('./data/temp/to_qr_qr.png','rb') as f:
        await interaction.response.send_message(f'{url}\nBy: {interaction.user.mention}',file = discord.File(f), ephemeral = eph)
    os.remove('./data/temp/to_qr_qr.png')
    fx.stats()

tree.add_command(to_qr)
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
