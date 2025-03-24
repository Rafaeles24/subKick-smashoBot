import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from events.setKickSub import setKickSub
from events.expiredKickSub import expiredKickSub
from command.test import commandTest
from command.setChannel import commandSetChannel
from command.setRole import commandSetRole
from discord import app_commands
from discord.ext import tasks
import datetime

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILDID = os.getenv("DISCORD_GUILD_ID")

intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    print(f"[Client] Bot live! {client.user}")

    if not client.application_id:
        client.application_id = (await client.application_info()).id

    try:
        synced = await client.tree.sync()
        await verificarSubExpirado.start()
        print(f"[Slash commands] Slash Commands sincronizados: {len(synced)}")
    except Exception as e:
        print(f"Error al sincronizar comandos: {e}")

@client.event
async def on_message(message):
    await setKickSub(message)

@tasks.loop(time=datetime.time(hour=0, minute=0, second=0))
async def verificarSubExpirado():
    await expiredKickSub(client, int(GUILDID))


@client.tree.command(name="test", description="Comando de prueba")
async def test(interaction: discord.Integration):
    await commandTest(interaction)

@client.tree.command(name="set-channel", description="Fija un canal donde el bot reconocera las imagenes")
@app_commands.default_permissions(administrator=True)
async def setChannel(interaction: discord.Integration):
    await commandSetChannel(interaction)

@client.tree.command(name="set-role", description="Fija un rol de subscripcion")

@app_commands.default_permissions(administrator=True)
@app_commands.describe(role="Selecciona el rol")
async def setRole(interaction: discord.Integration, role: discord.Role):
    await commandSetRole(interaction, role)
    
client.run(TOKEN)