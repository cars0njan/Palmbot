@app_commands(description="Send anonymous message to the wall")
@app_commands.describe(hide_identifier="Identifiers (#xxxx) let others regoninize your messages without revaliing your identity")
async def palmwall(
    interaction: discord.Interaction, 
    message: str, 
    hide_identifier = False,
    file=disocrd.File=None
):
    
    hash_id = hashlib.sha1.update(
        str(interaction.user.id).encode()
    ).hexdigest()
    hash_id = str(hash_id)

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
    clones = clones.to_list()
    
    if df[df["User_ID_Hash"] == hash_id].empty:
        df = df.append({"User_ID_Hash": hash_id, 'Banned':0})
    elif df[df["User_ID_Hash"] == hash_id]['Banned'][0]=='1':
        await interaction.response.send_message("error - Rejected\nYou are banned from using this command due to previous abuse\n\n*(contact developer by `/contact` if you think it is a mistake)*", ephemeral=True)
        return

    if not hide_identifier:
        identifier = df[df["User_ID_Hash"] == hash_id]['User_Identifier'][0]
        message=f"*#{hash_id.zfill(4)}*:\n{message}"
    else:
        message=f"*Guest*:\n{message}"

    channel = client.get_channel(text.open_id['PalmWall_Channel_ID'])
    sent_msg = await channel.send(message, file = file)
    
    for i in clones:
        channel = client.get_channel(text.open_id['PalmWall_Channel_ID'])
        await channel.send(message, file = file)
    
    await interaction.response.send_message(f"Message sent in\n{sent_msg.jump_url}\n\n*(join by typing `/help` if you are not in the server)*", ephemeral = True)
    fx.stats()

tree.add_command(palmwall)
    # await asyncio.sleep(randrange(,5))
    
    # await interaction.response.send_message(message, ephemeral=True)
    # await interaction.followup.send(message, ephemeral=True)