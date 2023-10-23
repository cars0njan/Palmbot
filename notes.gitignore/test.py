

@app_commands.comand(
    description = 'Schedule a message in this channel'
)
@app_commands.describe(
    message = 'The message you want to schedule',
    minute = 'Minute. Zero-padded in 2 digits. Default to be current minute',
    hour = '24-Hour in Van-time. Zero-padded in 2 digits. Default to be current hour',
    day = 'Day. Zero-padded in 2 digits. Default to be current day',
    month = 'Month. Zero-padded in 2 digits. Default to be current month',
    year = 'Year. Zero-padded in 4 digits. Default to be current year',
)
async schedule_message(
    interaction:discord.Interaction,
    message:str,
    minute_(MM): int = int(datetime.now(tz=pytz.timezone('America/Vancouver')).strtime('%M')),
    hour_(HH): int = int(datetime.now(tz=pytz.timezone('America/Vancouver')).strtime('%H')),
    day_(dd): int = int(datetime.now(tz=pytz.timezone('America/Vancouver')).strtime('%d')),
    month_(mm): int = int(datetime.now(tz=pytz.timezone('America/Vancouver')).strtime('%m')),
    year_(yyyy): int = int(datetime.now(tz=pytz.timezone('America/Vancouver')).strtime('%Y'))
):
    if interaction.user != interaction.guild.owner and not fx.has_role(interaction.user,"Admin_Palmbot"):
        await interaction.response.send_message('error - no permission\ncommand only for server owner or users with `Admin_Palmbot` role', ephemeral=True)
        return
    
    try:
        date  = datetime(year_(yyyy), month_(mm), day_(dd),hour_(HH), minute_(MM), tzinfo= pytz.timezone('America/Vancouver'))
        utc_date = date.astimezone(pytz.utc)
        utc_date = utc_date.strftime('%Y-%m-%d_%H:%M')

        key = os.environ['KEY']
        fernet = Fernet(key)
        e_message = fernet.encrypt(message.encode())
        e_channel = fernet.encrypt(str(interaction.channel.id).encode())

        df_a_data = {
            'MESSAGE': e_message,
            "CHANNEL": e_channel,
            "UTC_DATETIME": utc_date,
            "USER_ID": interaction.user.id,
            "SENT":0
        }
        
        df = pd.read_csv('./dada/encrypted/schedule.csv' , index_col='INDEX')
        df.loc[len(df)] = df_a_data
        df.to_csv('./dada/encrypted/schedule.csv',index_label = 'INDEX')

        await interaction.response.send_message(f'Sucessfully scheduled at\n{date.strftime('%Y-%m-%d_%H:%M')\n{message}}',ephemeral=True)
        fx.stats()

        #await interaction.response.send_message('message scheduled', ephemeral=True)
    except:
        await interaction.response.send_message('error - Invalid datetime', ephemeral=True)
        raise

#######################
        
@tasks.loop(minutes=1.0)
async def run_schedule_message():
    schedule = pd.read_csv('./dada/encrypted/schedule.csv' , index_col='INDEX')
    if len(schedule) > 0:
        pop_index = []
        for index, row in schedule.iterrows():
            try:
                utc_date  = datetime.strptime(row['UTC_DATETIME'], '%Y-%m-%d_%H:%M')
                now_utc_date = datetime.now(tz=pytz.utc)
                sent = row['SENT']
                
                if now_utc_date - utc_date >= timedelta(0) and sent == 0:
                    key = os.environ['KEY']
                    fernet = Fernet(key)
    
                    message = fernet.decrypt(row['MESSAGE']).decode()
                    channel = int(fernet.decrypt(row['CHANNEL']).decode())
                    user_id = int(fernet.decrypt(row['USER_ID']).decode())

                    channel = client.get_channel(channel)
                    user = client.get_user(user_id)
                    sent_msg = await channel.send(f'**{user.name}**:\n{message}')
                    pop_index = pop_index.append(index)

                    user.create_dm().send(f'Your scheduled message was sent\n{sent_msg.jump_url}')
            except:
                raise
            
        schedule.drop(pop_index,inplace=True)
        schedule.to_csv('./dada/encrypted/schedule.csv',index_label = 'INDEX')
    else:
        pass