from controller.subConfigController import createOrUpdateConfig

async def commandSetRole(interaction, role):
    try:
        guildId = interaction.guild.id
        roleId = role.id
        roleOrChannel = "role"

        response = await createOrUpdateConfig(guildId, roleId, roleOrChannel)
        return await interaction.response.send_message(response)
    
    except Exception as e:
        print(e)