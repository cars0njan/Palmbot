from cryptography.fernet import Fernet

key = os.environ['KEY']
fernet = Fernet(key)

@app_commands.command(
    description= 'set server welcome message lifespan | disable welcome message'
)
@app_commands.describe(
    lifespan = 'Minutes before the welcome message is deleted. Default to be 1. Set 0 to disable'
)

async def welcome_message_set(
    interaction:discord.Interaction,
    lifespan:int
):
    user = interaction.user
    perms = user.guild.permissions_for(user)
    if (not perms.administrator) or (not user.guild.owner = user):
        interaction.response.send_message('error - cmd only for admin/ server owner', ephemermal= True)
        return
    e_guild_id = fernet.encrypt(str(interaction.guild.id).encode())

    e_guild = pd.read_csv(
    "./data/encrypted/on_member_join.csv",
    index_col = 'ID'
)
    target = e_guild[e_guild['Guid_ID'] == e_guild_id]
    if result.empty():
        pass
    else:
        target['Lifespan'] = lifespan


