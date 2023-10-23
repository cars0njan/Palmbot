import os
import csv
import pandas as pd
import discord
from discord import app_commands
from datetime import datetime
import pytz

def read_tail_index(file_path):
    with open(file_path, 'r') as f:
        for line in f:
            pass
        
        return line.split(',')[0].replace('"','')

def csv_append(file_path, data):
    with open(file_path, 'a') as csv_file:
        csv_file.write(data)
        csv_file.write('\n')

def add_file(file_path, name, data):
    with open(file_path,name, 'w') as add_file:
        add_file.write(data)

def stats():
    stats_csv = pd.read_csv('./data/stats.csv')
    stats_csv.Command_runs[0] = stats_csv.Command_runs[0] + 1
    stats_csv.to_csv("./data/stats.csv", index=False)

def is_owner():
    def predicate(interaction: discord.Interaction):
        id_owner = os.environ['ID-OWNER']
        return interaction.user.id == int(id_owner)
    return app_commands.check(predicate)

def datetime_van():
    utc_now = datetime.utcnow()
    vancouver_timezone = pytz.timezone('America/Vancouver')
    vancouver_time = utc_now.replace(tzinfo=pytz.utc).astimezone(vancouver_timezone)
    return vancouver_time

def has_role(member,role_name:str):
    roles = member.roles
    for i in roles:
        if i.name == role_name:
            return True
    return False

# async def restart():
#     async def restarter():
#         os.system("python restarter.py")
#         os.system('kill 1')