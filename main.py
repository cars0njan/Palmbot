import os
from typing import Literal
import asyncio
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

import pandas as pd
import qrcode
import requests
from bs4 import BeautifulSoup as BS

from cryptography.fernet import Fernet
import hashlib

import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import tasks

#from discord.ext import commands
import alive
import functions as fx
import text

intents = discord.Intents.all()
#intents.message_content = True

#client = commands.Bot(command_prefix='=',intents=intents)

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)



# @tasks.loop(minutes=10.0)
# async def self_ping():
#     requests.head('https://palmbot.cars0njan.repl.co')
#     print('\n\nself_ping\n\n')

@client.event
async def on_ready():
    print('\n\nWe have logged in as {0.user}\n\n'.format(client))
    # self_ping.start()
    
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

@client.event
async def on_member_join(member):
    async with member.guild.system_channel.typing():
        await asyncio.sleep(1.5)
    welcome = f"Hello {member.mention}!\nA warm welcome from **{member.guild.name}**.\n\nPalmbot is here to bring you handy functions for your school life. Type `/` anytime to call a command.*\nWe also suggest you to join help server https://discord.gg/YHJx6dM6KH so that you can wake bot in case it is offline*\n\nEnjoy your time in this server!"
    await member.guild.system_channel.send(welcome, delete_after=60.0)
    fx.stats()
#####
@tree.command(description='List all commands avaliable')
async def all_commands(interaction:discord.Interaction):
    await interaction.response.send_message(f'**Here are all Palmbot commands**\n{text.all_commands}', ephemeral=True)

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

@tree.command(description='join help server')
async def help(interaction: discord.Interaction):
    text = text.open_id['Palmbot_join_url']
    await interaction.response.send_message(text, ephemeral = True)
    fx.stats()
#####
@app_commands.command(description='AP-Calculus day for today & tomorrow') #| your next AP-Cal class')
# @app_commands.describe(search_next='Which day are you in? We will show you your next class')

async def ap_cal(interaction:discord.Interaction):
    current_month = fx.datetime_van().strftime('%b')
    next_month = fx.datetime_van() + relativedelta(months=1)
    next_month = next_month.strftime('%b')
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
    
    if current_month in [1,3,5,7,8,10,12] and current_day ==31:
        next_str = f'{next_month}. 1 -'.lower()
    elif current_month in [4,6,9,11] and current_day ==30:
        next_str = f'{next_month}. 1 -'.lower()
    elif current_month == 2 and current_day == 28:
        next_str = f'{next_month}. 1 -'.lower()
    else:
        next_str = f'{current_month}. {current_day+1} -'.lower()
    
    def search_span(span_text, target):
        for i in span_text:
            if i.startswith(target):
                return i
        return 'No-Class'

    today_str = search_span(span_text, current_str)
    tmr_str = search_span(span_text, next_str)
    
    await interaction.response.send_message(f'AP-Calculus\nToday: **{today_str.title()}**\nTomorrow: **{tmr_str.title()}**', ephemeral=True)
    fx.stats()
    return

tree.add_command(ap_cal)

#####
@tree.command(description = 'Show school map')
async def map(interaction:discord.Interaction):
    file = discord.File('./data/upload/School_Map.png')
    await interaction.response.send_message(file=file, ephemeral = True)
    fx.stats()

#####
@tree.command(description = 'Show school bell schedule')
async def bell(interaction:discord.Interaction):
    file = discord.File('./data/upload/School_Bell.png')
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
    with open('./data/temp/invite_qr.png','rb') as f:
        await interaction.response.send_message(f'{invite_url}', file = discord.File(f), ephemeral = eph)
    os.remove('./data/temp/invite_qr.png')
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
    fx.stats()
    os.remove('./data/temp/to_qr_qr.png')

tree.add_command(to_qr)
#####

@app_commands.command(description='show a link to log volunteer hours')
async def volunteer_hours (interaction:discord.Interaction):
    key = os.environ['KEY']
    fernet = Fernet(key)

    hash_guild_id = hashlib.sha1(str(interaction.guild.id).encode()).hexdigest()
    hash_guild_id = str(hash_guild_id)

    df = pd.read_csv('./data/encrypted/volunteer_hours.csv',index_col='INDEX')
    df_row = df[df['Hashed_Guild_ID'] == hash_guild_id].values.tolist()
    print(df_row)

    if len(df_row) ==0:
        await interaction.response.send_message('error - NullValue\nThere is no link set for you server', ephemeral=True)
        return
    else:
        e_link = df_row[0][2]
        e_link = e_link[2:len(e_link)].encode()
        link = fernet.decrypt(e_link).decode()

        await interaction.response.send_message(f'Log Volunteer Hours\n{link}', ephemeral=True)
        fx.stats()

tree.add_command(volunteer_hours)

#####

@app_commands.command(
    description="set a link to show by `/volunteer_hours` in this server"
)
@app_commands.describe(
    url="Please make sure that your link is appropriate for your server"
)
async def volunteer_hours_set (interaction:discord.Interaction, url: str):
    if interaction.user != interaction.guild.owner and not fx.has_role(interaction.user,"Admin_Palmbot"):
        await interaction.response.send_message('error- no permission\ncommand only for server owner and users with Admin_Palmbot role')
        return

    key = os.environ['KEY']
    fernet = Fernet(key)

    hash_guild_id = hashlib.sha1(str(interaction.guild.id).encode()).hexdigest()
    hash_guild_id = str(hash_guild_id)

    df = pd.read_csv('./data/encrypted/volunteer_hours.csv',index_col='INDEX')
    df_row = df[df['Hashed_Guild_ID'] == hash_guild_id].values.tolist()


    e_guild_id = fernet.encrypt(str(interaction.guild.id).encode())
    e_guild_id = str(e_guild_id)
    e_url = fernet.encrypt(url.encode())
    e_url = str(e_url)
    hash_url = hashlib.sha1(url.encode()).hexdigest()
    hash_url = str(hash_url)
    e_set_user_id = fernet.encrypt(str(interaction.user.id).encode())
    e_set_user_id = str(e_set_user_id)

    df_a_data = {
        "Encrypted_Guild_ID": e_guild_id,
        "Hashed_Guild_ID": hash_guild_id,
       "Encrypted_url": e_url, 
        "Hashed_url": hash_url,
        "Encrypted_set_user_id": e_set_user_id
}
    if len(df_row) == 0:
        df.loc[len(df)] = df_a_data

        df.to_csv(
            "./data/encrypted/volunteer_hours.csv",
            index_label="INDEX"
        )
        await interaction.response.send_message(f"successfully added", ephemeral = True)
        return
        fx.stats()
    else:
        df_row_id = df[df['Hashed_Guild_ID']== hash_guild_id].index.values[0]
        print(df_row_id)
        df.loc[df_row_id] = df_a_data

        df.to_csv(
            "./data/encrypted/volunteer_hours.csv",
            index_label="INDEX"
        )
        await interaction.response.send_message("successfully updated", ephemeral=True)
        return
        fx.stats()

tree.add_command(volunteer_hours_set)
#####

@app_commands.command(description="Send anonymous message to the wall")
@app_commands.describe(show_identifier="Showing identifier (#xxxx) can proof youself the same person a across messages. This also makes you trackable across messages.")
async def palmwall(
    interaction: discord.Interaction, 
    message: str, 
    show_identifier:Literal['True','False'] = '',
    file:discord.Attachment=None
):
    if not file == None:
        # file = await raw_file.to_file()
        filetype= file.content_type.split('/')[-1]
        await file.save(f'./data/temp/SPOILER_wall.{filetype}')
    hide_identifier = not bool(show_identifier)
    hash_id = hashlib.sha1(
        str(interaction.user.id).encode()
    ).hexdigest()
    hash_id = str(hash_id)
    channel = client.get_channel(int(text.open_id['PalmWall_Channel_ID']))

    df = pd.read_csv(
        "./data/encrypted/palmwall.csv",
        index_col="User_Identifier",
        dtype = 'str'
    )

    clones = pd.read_csv(
        "./data/palmwall_clones.csv",
        index_col = False,
        dtype = 'str'
    )
    clones = clones['Channel_ID'].to_list()
    
    # print(f'\n\n{type(df)}\n\n')
    if df[df["User_ID_Hash"] == hash_id].empty:
        df.loc[len(df)] = {"User_ID_Hash": hash_id, 'Banned':0}
        df.to_csv(
            "./data/encrypted/palmwall.csv",
            index_label="User_Identifier"
        )
    elif df[df["User_ID_Hash"] == hash_id]['Banned'][0]=='1':
        await interaction.response.send_message("error - Rejected\nYou are banned from using this command due to previous abuse\n\n*(contact developer by `/contact` if you think it is a mistake)*", ephemeral=True)
        return

    if not hide_identifier:
        identifier = df[df["User_ID_Hash"] == hash_id]
        identifier =str(identifier.index[0])
        message=f"*#{identifier.zfill(4)}*:\n{message}\n."
    else:
        key = os.environ['KEY']
        fernet = Fernet(key)
        e_id = fernet.encrypt(str(interaction.user.id).encode())
        e_id = str(e_id)[2:-1]
        message=f"`{e_id}`:\n{message}"
    
    channel = client.get_channel(int(text.open_id['PalmWall_Channel_ID']))
    if not file == None:
        #with open(f'./data/temp/SPOILER_wall.{filetype}', 'rb') as f:
        f = discord.File(f'./data/temp/SPOILER_wall.{filetype}')
        sent_msg = await channel.send(message, file = f)
    else:
        sent_msg = await channel.send(message)
    
    await interaction.response.send_message(f"Message sent in\n{sent_msg.jump_url}\n\n*(join by typing `/help` if you are not in the server)*", ephemeral = True)
    fx.stats()

    if not clones:
        return
    if not file == None:
        # with open(f'./data/temp/SPOILER_wall.{filetype}', 'rb') as f:
        for i in clones:
            try:
                channel = client.get_channel(int(i))
                f = discord.File(f'./data/temp/SPOILER_wall.{filetype}')
                await channel.send(message, file = f)
            except:
                pass
        os.remove(f'./data/temp/SPOILER_wall.{filetype}')
    else:
        for i in clones:
            try:
                channel = client.get_channel(int(i))
                await channel.send(message)
            except:
                pass

tree.add_command(palmwall)
#####
@app_commands.command(description="Make this channel a clone of PalmWall")
async def palmwall_clone (interaction:discord.Interaction):
    if interaction.user != interaction.guild.owner and not fx.has_role(interaction.user,"Admin_Palmbot"):
        await interaction.response.send_message('error- no permission\ncommand only for server owner and users with Admin_Palmbot role')
        return
    
    clones = pd.read_csv(
        "./data/palmwall_clones.csv",
        index_col = 'INDEX',
        dtype = 'str'
    )

    if clones[clones['Channel_ID'] == str(interaction.channel.id)].empty:
        clones.loc[len(clones)] = {'Channel_ID':str(interaction.channel.id)}
        clones.to_csv(
            "./data/palmwall_clones.csv",
            index_label = 'INDEX'
        )
        await interaction.response.send_message('sucessfully cloned',ephemeral=True)
        msg = await interaction.channel.send(text.text['clone'])
        await msg.pin()
    else:
        await interaction.response.send_message("error - Invalid\nChannel already cloned",ephemeral=True)

tree.add_command(palmwall_clone)
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
