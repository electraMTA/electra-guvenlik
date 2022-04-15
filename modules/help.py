import discord 
from discord.ext import commands

class Yardım(commands.Cog):
    
    def __init__(self, client) -> None:
        self.client = client 

    @commands.Cog.listener()
    async def on_ready(self):
        print('electraGüvenlik - Yardım komudu yüklendi!')

    @commands.command()
    async def yardım(self, ctx):
        embed = discord.Embed(
            title = 'electraGüvenlik - Yardım',
            description = 'Sunucu ve veritabanı güvenliği hakkındaki komutlar.',
            colour = discord.Colour.blue()
        )
        sender = ctx.message.author
        embed.set_footer(text=f'{sender.name} tarafından istendi.', icon_url=sender.avatar_url)
        embed.set_thumbnail(url=self.client.user.avatar_url)

        embed.add_field(name='eguvenlik logyedegi', value='Sunucunun log yedeği hakkındaki komutlar', inline=False)
        embed.add_field(name='eguvenlik paketyedegi', value='Sunucunun paket yedeği hakkındaki komutlar', inline=False)
        embed.add_field(name='eguvenlik veriyedegi', value='Sunucunun veri yedeği hakkındaki komutlar', inline=False)

        await ctx.reply(embed=embed, mention_author=True)

def setup(client):
    client.add_cog(Yardım(client))