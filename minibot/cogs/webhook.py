import discord
import asyncio
from discord.ext import commands
from discord import Webhook, AsyncWebhookAdapter
import aiohttp
import json
import random
import json
def savedata(data):
    with open('./file/mybot.json', 'w', encoding='utf-8') as make_file:
        json.dump(data, make_file, indent="\t", ensure_ascii=False)

async def send(url, username = None , avatar_url = None , text=None, embed = None):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(url, adapter=AsyncWebhookAdapter(session))
        await webhook.send(username = username , avatar_url = avatar_url , content=text, embed = embed)

class webhook (commands.Cog) :
    def __init__ (self, bot) :
        self.bot = bot
        self.data = dict()
        self.clipboard = dict()
        asyncio.get_event_loop().create_task(self.on_load())

    async def on_load(self):
        await self.bot.wait_until_ready()
        with open('./file/mybot.json', 'r', encoding='UTF8') as f:
            self.data = json.load(f)

    @commands.command()
    async def 자동등록(self, ctx):
        wh = await ctx.channel.create_webhook(name='Minibot_Mybot Webhook' , reason='자동으로 생성된 미니봇의 마이봇 기능 전용 웹훅입니다.')
        self.data[str(ctx.channel.id)] = dict()
        self.data[str(ctx.channel.id)]['names'] = list()
        self.data[str(ctx.channel.id)]['prefixs'] = dict()
        self.data[str(ctx.channel.id)]['url'] = wh.url
        await ctx.send(f'<#{str(ctx.channel.id)}> 채널을 DB에 적용시켰어요!')
        savedata(self.data)


    @commands.command()
    async def 등록(self, ctx, url):
        self.data[str(ctx.channel.id)] = dict()
        self.data[str(ctx.channel.id)]['names'] = list()
        self.data[str(ctx.channel.id)]['prefixs'] = dict()
        self.data[str(ctx.channel.id)]['url'] = url
        await ctx.send(f'<#{str(ctx.channel.id)}> 채널을 DB에 적용시켰어요!')
        savedata(self.data)

    @commands.command()
    async def 생성(self, ctx, name ,prefix):
        if name in self.data[str(ctx.channel.id)]['names'] or prefix in list(self.data[str(ctx.channel.id)]['prefixs'].keys()):
            await ctx.send(f'이런! 이름 또는 프리픽스가 다른 봇과 겹쳐요')
        else:
            self.data[str(ctx.channel.id)][name] = dict()
            self.data[str(ctx.channel.id)][name]['name'] = name
            self.data[str(ctx.channel.id)][name]['prefix'] = prefix
            self.data[str(ctx.channel.id)][name]['avatar'] = None
            self.data[str(ctx.channel.id)][name]['cmd'] = dict()
            self.data[str(ctx.channel.id)][name]['owner'] = ctx.author.id

            self.data[str(ctx.channel.id)]['names'].append(name)
            self.data[str(ctx.channel.id)]['prefixs'][prefix] = name

            await ctx.send(f'이 채널에 봇을 만들었어요!\n```봇 이름 : {name}\n프리픽스 : {prefix}```')
            savedata(self.data)
    
    @commands.command()
    async def 커맨드생성(self, ctx, name ,a,b):
        if self.data[str(ctx.channel.id)][name]['owner'] == ctx.author.id:
            self.data[str(ctx.channel.id)][name]['cmd'][a] = b
            await ctx.send(f'커맨드 생성 완료!')
            savedata(self.data)
        else:
            await ctx.send(f'이런! 봇의 주인만 커맨드를 만들수 있어요!')

    @commands.command()
    async def 프사변경(self, ctx, name, au):
        if self.data[str(ctx.channel.id)][name]['owner'] == ctx.author.id:
            self.data[str(ctx.channel.id)][name]['avatar'] = au
            await ctx.send(f'성공!')
            savedata(self.data)
        else:
            await ctx.send(f'이런! 봇의 주인만 프사를 바꿀 수 있어요!')

    @commands.command()
    async def 봇정보(self, ctx, name):
        if name in self.data[str(ctx.channel.id)]['names']:
            data = self.data[str(ctx.channel.id)][name]
            embed = discord.Embed(title=name)
            embed.add_field(name='봇 오너', value=ctx.guild.get_member(int(data['owner'])).display_name)
            embed.add_field(name='프리픽스', value=data['prefix'])
            embed.add_field(name='커맨드', value=f"```{', '.join(list(data['cmd'].keys()))}```")
            if data['avatar'] == None:
                pass
            else:
                embed.set_thumbnail(url=data['avatar'])
            await ctx.send(embed = embed)
            savedata(self.data)

    @commands.command()
    async def 복사(self, ctx, name):
        if self.data[str(ctx.channel.id)][name]['owner'] == ctx.author.id:
            code = random.randint(1000,9999)
            self.clipboard[code] = self.data[str(ctx.channel.id)][name]
            await ctx.send(f'봇을 복사했어요! 원하는 채널에 가서 `미니봇 붙여넣기 {code}` 를 해주세요!')
        else:
            await ctx.send(f'이런! 봇의 주인만 봇을 복사할 수 있어요!')

    @commands.command()
    async def 붙여넣기(self, ctx, code:int):
        if self.clipboard.get(code) == None:
            await ctx.send(f'유효하지 않은 코드에요')
        else:
            if self.clipboard[code]['owner'] == ctx.author.id:
                name = self.clipboard[code]['name']
                prefix = self.clipboard[code]['prefix']
                if name in self.data[str(ctx.channel.id)]['names'] or prefix in list(self.data[str(ctx.channel.id)]['prefixs'].keys()):
                    await ctx.send(f'이런! 이름이나 프리픽스가 겹쳐요!')
                else:
                    self.data[str(ctx.channel.id)][name] = self.clipboard[code]
                    await ctx.send(f'복사 완료!')
                    savedata(self.data)
            else:
                await ctx.send(f'이런! 봇의 주인만 봇을 복사할 수 있어요!')

    @commands.Cog.listener()
    async def on_message(self, message):
        msg = message.content
        try:
            for i in list(self.data[str(message.channel.id)]['prefixs'].keys()):
                lenn = len(i)
                if i == msg[:lenn]:
                    cm = msg[lenn:]
                    name = self.data[str(message.channel.id)]['prefixs'][i]
                    if cm in self.data[str(message.channel.id)][name]['cmd']:
                        avatar = self.data[str(message.channel.id)][name]['avatar']
                        await send(self.data[str(message.channel.id)]['url'], name, avatar, self.data[str(message.channel.id)][name]['cmd'][cm])
        except:
            pass

def setup (bot) :
    bot.add_cog (webhook (bot))
    print ('webhook Loaded!')