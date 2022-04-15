import discord
import os 

from discord.ext import commands

client = commands.Bot(command_prefix='eguvenlik ')

@client.event
async def on_ready():
    print('electraMTA, {0.user}; aktive edildi.'.format(client))
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

@client.command()
async def load(ctx, extension):
    client.load_extension(f'modules.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'modules.{extension}')

for cog in os.listdir('./modules'):
    if cog.endswith('.py'):
        client.load_extension(f'modules.{cog[:-3]}')

client.run('OTYzODgyMTI3NzE4NDg2MDE2.YlcjLw.GhpnL8DOZpjBOhB3FStwVcfVIZ0')