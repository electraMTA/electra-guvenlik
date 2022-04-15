from email.mime import base
from random import randint
import discord 
import os
import datetime
import base64
import time
from github import Github
from discord.ext import commands

TOKEN = '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'
git = Github(TOKEN)
user = git.get_user()
org = git.get_organization('electraMTA')
backupRepo = org.get_repo('electrabackups')

class VeriYedeği(commands.Cog):
    
    def __init__(self, client) -> None:
        self.client = client 

    @commands.Cog.listener()
    async def on_ready(self):
        print('electraGüvenlik - veriyedegi komudu yüklendi!')

    @commands.command()
    async def veriyedegi(self, ctx, method=None, dbName=None, downName=None):
        sender = ctx.message.author
        channel = self.client.get_channel(963892657556443176)
        if sender.id in (916435638977437746, 921838160332349471, 903002363638460416): # vio, bird, astreal
            if method == None or method.lower() not in ('al', 'kurtar', 'htemizle', 'listele', 'get', 'save', 'clear', 'list'):

                embed = discord.Embed(
                    title = 'electraGüvenlik - Veri Yedeği',
                    description = 'Sunucunun veri yedeği hakkındaki komutlar.',
                    colour = discord.Colour.blue()
                )
                
                embed.set_footer(text=f'{sender.name} tarafından istendi.', icon_url=sender.avatar_url)
                embed.set_thumbnail(url=self.client.user.avatar_url)

                embed.add_field(name='eguvenlik veriyedegi al', value='Sunucunun veri yedeğini anlık olarak alır.', inline=False)
                embed.add_field(name='eguvenlik veriyedegi kurtar', value='Sunucunun geçmiş veri yedeklerinden birisini kurtarır.', inline=False)
                embed.add_field(name='eguvenlik veriyedegi htemizle', value='Sunucunun veri yedek geçmişini temizler (Kurtarılamaz yapar.)', inline=False)
                embed.add_field(name='eguvenlik veriyedegi listele', value='Sunucunun veri yedek geçmişini listeler.', inline=False)

                await ctx.reply(embed=embed, mention_author=True)
            else:

                method = method.lower()
                self.curPath = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + r'\veriyedekleri'

                
                if method == 'al' or method == 'get':
                    dbName = dbName or 'electradb'
                    await ctx.reply(f'{dbName} yedeklenmesi için sunucuya istek gönderildi. [22003]')
                    start = time.time()
                    expectedFilePath = self.curPath + r'\{}.sql'.format(dbName)
                    process =  os.system('mysqldump --no-defaults -u {} -p{} {} > {}'.format('root', '123456789', dbName, expectedFilePath),)
                    result = 'İşlem başarısızlıkla sonuçlandı'
                    if os.path.isfile(expectedFilePath):
                        result = 'Özelden veri yedeği ulaştırıldı ve Github üzerine kayıt yapıldı.'
                        with open(expectedFilePath, 'r', encoding="mbcs") as sqlFile:
                            content = sqlFile.read() # wiki-14.04.2022|2.39.sql
                            timeStamp = getCurrentTimeStamp()
                            backupRepo.create_file(f'veriyedekleri/{dbName}-{timeStamp}.sql', 'discord internal commit', content, 'main')
                            baseURL = f'https://github.com/electraMTA/electrabackups/blob/main/veriyedekleri/{dbName}-{timeStamp}.sql'
                            end = time.time()
                            result = result + f'. İşlem {end - start} sn sürdü.'
                            await sender.send(f'Github linki: {baseURL}\nLütfen bu linki kimseyle paylaşmayın.')
                            await channel.send(f'{sender.name}#{sender.discriminator} isimli kullanıcı {dbName} veritabanının yedeğini aldı.')
                        
                        os.remove(expectedFilePath)
                    else:
                        await channel.send(f'{sender.name}#{sender.discriminator} isimli kullanıcı "{dbName}" veritabanının yedeğini almaya çalıştı.')
                    await ctx.reply(f'Sunucudan dönüt: {process}\n{result}')
                elif method == 'listele' or method == 'list':
                    await ctx.reply('Github üzerindeki yedekler getiriliyor, lütfen bekleyiniz. [22003]')
                    contents = backupRepo.get_contents('veriyedekleri')
                    contents_List = [path.path for path in contents if path.path.endswith('sql')]
                    embed = discord.Embed(
                        title = 'electraGüvenlik - Veri Yedeği Kayıtları',
                        description = 'Sunucunun veri yedeğinin saklanan kayıtları',
                        colour = discord.Colour.blue()
                    ) 
                
                    embed.set_footer(text=f'{sender.name} tarafından istendi.', icon_url=sender.avatar_url)
                    embed.set_thumbnail(url=self.client.user.avatar_url)
                    for index, content in enumerate(contents_List):
                        # "veriyedekleri/wiki-14.04.2022|2.22"
                        baseName = content.split('/')[1][:-4]
                        # wiki-14.04.2022|2.22"
                        dbName, cDate = tuple(baseName.split('-'))
                        cEDate = cDate
                        cDate = datetime.datetime.strptime(cDate, '%d.%m.%Y|%H.%M')
                        nowDate = datetime.datetime.now()
                        substracted = abs((nowDate - cDate))
                        val = f'{substracted.days} gün önce alındı'
                        if substracted.days < 1:
                            hours, min = 0, 0
                            if substracted.seconds >= 60:
                                mins = substracted.seconds // 60
                                if mins >= 60:
                                    hours = substracted.seconds // 60
                                    mins = substracted.seconds % 60
                                    
                            else:
                                mins = 1
                                
                            val = f'{hours} saat ve {mins} dakika önce alındı ({cEDate})'
                        embed.add_field(name=f'{index}. {dbName}', value=val, inline=True)
                            
                    await ctx.reply(embed=embed)
                elif method == 'kurtar' or method == 'save':
                    if dbName and dbName.isdigit():
                        dbName = int(dbName)
                        contents = backupRepo.get_contents('veriyedekleri')
                        contents_List = [path.path for path in contents if path.path.endswith('sql')]
                        if len(contents_List) - 1 >= dbName:
                            start = time.time()
                            await ctx.reply('Veri yedeği kurtarılmaya başlandı! [22003]')
                            path = contents_List[dbName]
                            try:
                                contents = backupRepo.get_contents(path)
                            
                            except:
                                contents = get_blob_content(backupRepo, 'main', path)
                            fileContent = contents.content 
                            fileName = path.split('/')[1]
                            if not downName:
                                downName = f'yedek-{randint(1000, 9999)}' 
                            fileContent = base64.b64decode(fileContent)
                            with open(f'veriyedekleri/{downName}.sql', 'wb') as tFile:
                                tFile.write(fileContent)
                            end = time.time()
                            size = os.path.getsize(f'veriyedekleri/{downName}.sql') / 10**6 
                            
                            await ctx.reply(f'Başarıyla {fileName} kurtarıldı. Dosya boyutu: {size} kb. İşlem {end - start} sn sürdü. [22003]')
                            await channel.send(f'{sender.name}#{sender.discriminator} isimli kullanıcı {fileName} veritabanı yedeğini kurtardı.')
                        else:
                            await ctx.reply('Böyle bir kayıt bulunamadı.')
                    else:
                        await ctx.reply('Bir index değeri girmeniz gerekiyor.')
                elif method == 'htemizle' or method == 'clear':
                    contents = backupRepo.get_contents('veriyedekleri')
                    contents_List = [path.path for path in contents if path.path.endswith('sql')]
                    if not dbName or dbName.lower() in ('all', 'hepsi'):
                        return 
                    elif dbName.isdigit() and int(dbName) <= len(contents_List) - 1:
                        dbName = int(dbName)
                        target = contents_List[dbName]
                        await ctx.reply(f'{target} isimli veri yedeği silinmeye başlandı! [22003]')
                        try:
                            contents = backupRepo.get_contents(target)
                            
                        except:
                            contents = get_blob_content(backupRepo, 'main', target)
                        fileContent = contents.content 
                        fileContent = base64.b64decode(fileContent).decode('utf-8')
                        fileName = target.split('/')[1][:-4]
                        print(fileName, len(fileContent))
                        backupRepo.delete_file(target, 'delete automation', fileContent, 'main')
                        await ctx.reply(f'Başarıyla {fileName} isimli veri yedeği silindi!')
                        await channel.send(f'{sender.name}#{sender.discriminator} isimli kullanıcı {fileName} veritabanı yedeğini sildi.')
                    else:
                        await ctx.reply('Böyle bir veri yedeği bulunamadı!')
                    return    
        else:
            await ctx.reply('Bunu gerçekleştirmek için yetkin yok!', mention_author=True)
            await channel.send(f'{sender.name}#{sender.discriminator} isimli kullanıcı veri yedeği almayı denedi! @everyone & @here!')

def getCurrentTimeStamp() -> str:
    now = datetime.datetime.now()
    return (
        now.strftime('%d.%m.%Y|%H.%M')
    )

def setup(client):
    client.add_cog(VeriYedeği(client))

def get_blob_content(repo, branch, path_name):
    ref = repo.get_git_ref(f'heads/{branch}')
    tree = repo.get_git_tree(ref.object.sha, recursive='/' in path_name).tree
    sha = [x.sha for x in tree if x.path == path_name]
    if not sha:
        return None
    return repo.get_git_blob(sha[0])