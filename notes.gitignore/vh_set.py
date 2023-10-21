from cryptography.fernet import Fernet
import hashlib

@app_commands.command(
    description="set a link to show by `/volunteer_hours` in this server"
)
async def(interaction:discord.Interaction, url:str):
    if interaction.user != interaction.guild.owner and not fx.has_role(interaction.user,"Admin_Palmbot")
        await interaction.response.send_message('error- no permission\ncommand only for server owner and users with Admin_Palmbot role')
        return

    key = os.environ['KEY']
    fernet = Fernet(key)

    e_guild_id = fernet.encrypt(str(interaction.guild.id).encode())

    df = pd.read_csv('./data/enncrypted/volunteer_hours.csv',index_col='INDEX')
    df_row = df[df['Encrypted_Guild_ID'== e_guild_id].values.tolist()

    e_url = fernet.encrypt(url.encode())
    hash_url = hashlib.sha1.update(url.encode()).hexdigest()

    df_a = {
       'Encrypted_Guild_ID': e_guild_id,
       'Encrypted_url': e_url, 
       'Hashed_url': hash_url
}
    if len(df_row) == 0:
        df = df.append(df_a, ignore_index=True)

        df.to_csv("./data/enncrypted/volunteer_hours.csv",index_label="Index")
        await interaction.response.send_message("success")
        return
        fx.stats()
    else:
        df_row_id = df[df['Encrypted_Guild_ID'== e_guild_id].index
        df.loc[df_row_id] = df_a

        df.to_csv("./data/enncrypted/volunteer_hours.csv",index_label="Index")
        await interaction.response.send_message("success")
        return
        fx.stats()