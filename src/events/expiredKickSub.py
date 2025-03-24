import discord
from controller.subConfigController import getSubConfig
from controller.subscripcionController import setExpiredSubscripciones, setRoleExpired

async def expiredKickSub(client, discord_guild_id):
    try:
        config = await getSubConfig(discord_guild_id)
        print("Configuracion del servidor obtenido.")
        guild = client.get_guild(config.discord_guild_id)
        if not guild:
            return
        
        expiredSubs = await setExpiredSubscripciones(discord_guild_id)

        if not expiredSubs:
            return print(f"No hay subscripciones expirados")
        
        channel = client.get_channel(config.discord_sub_channel_id)
        if not channel:
            return print(f"No se pudo obtener el canal con id: {config.discord_sub_channel_id}")

        for userId in expiredSubs:
            print("Intentando quitar roles...")
            member = guild.get_member(userId.discord_id)
            if not member: 
                return print(f"No se pudo encontrar al miembro con id: {userId.discord_id}")

            role = discord.utils.get(guild.roles, id=config.discord_sub_role_id)
            if not role: 
                return print(f"No se pudo encontrar el rol con id: {config.discord_sub_role_id}")
            
            if not role in member.roles:
                return print(f"El miembro con id: {member.id} no tiene el rol con id: {config.discord_sub_role_id}")

            await member.remove_roles(role)
            await setRoleExpired(member.id)

            await channel.send(f"{member.mention} tu subscripcion ha expirado.")

        return print("Evento sub expirado ejecutado.")
    except Exception as e:
        print(e)