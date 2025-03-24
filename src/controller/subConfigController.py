from config.db import get_db
from model.SubConfig import SubConfig

async def getSubConfig(discord_guild_id):
    db = next(get_db())

    try:
        config = db.query(SubConfig).filter(SubConfig.discord_guild_id == discord_guild_id).first()
        if not config:
            nuevaConfig = SubConfig(
                discord_guild_id = discord_guild_id
            )
            db.add(nuevaConfig)
            db.commit()

            return nuevaConfig

        return config
    except Exception as e:
        db.rollback()
        return f"❌ Error inesperado: {str(e)}"
    finally:
        db.close()

async def createOrUpdateConfig(discord_guild_id, discordRoleOrChannel, roleOrChannel):
    db = next(get_db())

    try:
        config = db.query(SubConfig).filter(SubConfig.discord_guild_id == discord_guild_id).first()

        if config:
            if roleOrChannel == "channel":
                config.discord_sub_channel_id = discordRoleOrChannel
            elif roleOrChannel == "role":
                config.discord_sub_role_id = discordRoleOrChannel
        else: 
            nuevaConfig = SubConfig(
                discord_guild_id = discord_guild_id,
                discord_sub_role_id = discordRoleOrChannel if roleOrChannel == "role" else None,
                discord_sub_channel_id = discordRoleOrChannel if roleOrChannel == "channel" else None
            )

            db.add(nuevaConfig)
        
        db.commit()

        return f"Configurarion de subscripcion actualizada"
    except Exception as e:
        db.rollback()
        return f"❌ Error inesperado: {str(e)}"
    finally:
        db.close()
