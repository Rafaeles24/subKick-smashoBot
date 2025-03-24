from controller.subConfigController import createOrUpdateConfig

async def commandSetChannel(interaction):
    try:
        channelId = interaction.channel.id
        guildId = interaction.guild.id
        roleOrChannel = "channel"
        
        response = await createOrUpdateConfig(guildId, channelId, roleOrChannel)
        return await interaction.response.send_message(response)
    except Exception as e:
        print(e)