import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from events.on_message import handle_message
from command.test import commandTest
from command.setChannel import commandSetChannel
from command.setRole import commandSetRole
from discord import app_commands

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    print(f"[Client] Bot live! {client.user}")

    if not client.application_id:
        client.application_id = (await client.application_info()).id

    try:
        synced = await client.tree.sync()
        print(f"[Slash commands] Slash Commands sincronizados: {len(synced)}")
    except Exception as e:
        print(f"Error al sincronizar comandos: {e}")

@client.event
async def on_message(message):
    await handle_message(message)

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