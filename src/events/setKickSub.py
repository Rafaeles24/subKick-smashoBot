import discord
import datetime
from functions.subImageRead import subImageRead
from controller.subscripcionController import createOrUpdateSub
from controller.subConfigController import getSubConfig

async def setKickSub(message):
    config = await getSubConfig(message.guild.id)

    if config.discord_sub_channel_id and message.channel.id != config.discord_sub_channel_id:
        return

    if message.attachments:
        for attachment in message.attachments:
            if attachment.filename.endswith((".png", ".jpg", ".jpeg")): 
                userId = message.author.id
                guildId = message.guild.id
                globalName = message.author.global_name
                tiempoActual = datetime.date.now().strftime("%Y-%m-%d")
                fileExtension = attachment.filename.split(".")[-1]
                fileName = f"{userId}-{tiempoActual}.{fileExtension}"
                imgPath = f"./src/temp/{fileName}"
                await attachment.save(imgPath)

                data = await subImageRead(imgPath)

                if data["nickname"] != globalName:
                    return await message.channel.send(f"{message.author.mention} -> El nombre de usuario en la imagen no se encontró o no coincide con tu nickname de Discord.")

                if data["canal_kick"] != "smashdota":
                    return await message.channel.send(f"{message.author.mention} -> No se ha encontrado el canal de smashdota en la imagen proporcionado.")
                
                if data["fecha_fin"] is None:
                    return await message.channel.send(f"{message.author.mention} -> No se ha encontrado la fecha de caducidad en la imagen proporcionado.") 
                
                if data["fecha_fin"] < tiempoActual:
                    return await message.channel.send(f"{message.author.mention} -> La fecha de caducidad ya paso.")

                # Registro de la subscripcion a la base de datos.
                response = await createOrUpdateSub(guildId, userId, globalName, data["fecha_inicio"], data["fecha_fin"])
                
                if response != "Success":
                    return await message.channel.send(response)

                #Gestion de roles de subscripcion
                if not config.discord_sub_role_id:
                    return await message.channel.send(f"No hay un rol fijado para establecer.")
                
                member = message.author
                role = member.guild.get_role(config.discord_sub_role_id)
                if role:
                    try:
                        await member.add_roles(role)
                        return await message.channel.send(f"¡{message.author.mention} -> Ahora tiene el rol de subscripción!")
                    except discord.Forbidden:
                        return await message.channel.send("❌ No tengo permisos suficientes para asignar este rol. Verifica que mi rol pueda administrar y esté por encima del rol que intentas asignar.")
                    except discord.HTTPException as e:
                        return await message.channel.send(f"❌ Ocurrió un error inesperado al asignar el rol: {e}")

                else:
                    return await message.channel.send("Algo malo ha sucedido")
