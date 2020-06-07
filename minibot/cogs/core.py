import discord
import asyncio
from discord.ext import commands, tasks
from tools.tools import emojicheck, get_emoji
from EZPaginator import Paginator
import requests
import base64, datetime
from bs4 import BeautifulSoup
from urllib import parse
import time, random, json
from run import START
from tools.requests import reqjson
import psutil, cpuinfo

def savedata(name, data):
    print(name)
    print(data)
    with open(f'./file/{name}.json', 'w', encoding='utf-8') as make_file:
        json.dump(data, make_file, indent="\t", ensure_ascii=False)

class Core (commands.Cog) :
    def __init__ (self, bot) :
       self.bot = bot
       self.messages = ['미니봇 도움', 'Minibox#1111']
       self.save = dict()
       asyncio.get_event_loop().create_task(self.on_load())

    @tasks.loop(seconds=15)
    async def status_loop(self):
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(name=self.messages[0], type=discord.ActivityType.playing))
        self.messages.append(self.messages.pop(0))
        await asyncio.sleep(15)

    async def on_load(self):
        await self.bot.wait_until_ready()
        self.status_loop.start()
        with open('./file/save.json', 'r', encoding='UTF8') as f:
            self.save = json.load(f)


    async def syncmember(self, guild):
        for i in self.member['channels']:
            ch = guild.get_channel(i)
            if ch is not None:
                print(ch)
                print(ch)
                print(f"[ 유저: {ch.guild.member_count}명 ]")
                await ch.edit(name=f"[ 유저: {ch.guild.member_count}명 ]")
                print(ch.name)
        

    @commands.Cog.listener()
    async def on_command_error(self, ctx, e):
        if str(type(e)) == "<class 'discord.ext.commands.errors.CheckFailure'>":
            await ctx.message.add_reaction('⛔')
            if await emojicheck('⛔', ctx, ctx.message) == True:
               await ctx.send(f'[ {ctx.message.content} ] 명령을 실행하기에 권한이 부족해요')
        elif str(type(e)) == "<class 'discord.ext.commands.errors.CommandNotFound'>":
            if ctx.message.content[:3] == '```':
                pass
            else:
                #await ctx.message.add_reaction('🤔')
                if await emojicheck('🤔', ctx, ctx.message) == True:
                    if ctx.message.content[0] == '`':  
                        cmdstart = ctx.message.content.split(' ')
                        cmdstart = cmdstart[0]
                        await ctx.send(f'[ {cmdstart} ] (은)는 없는 커맨드네요')
                    else:
                        cmdstart = ctx.message.content.split(' ')
                        cmdstart = cmdstart[1]
                        await ctx.send(f'[ {cmdstart} ] (은)는 없는 커맨드네요')
        else:
            await ctx.message.add_reaction('⚠')
            if await emojicheck('⚠', ctx, ctx.message) == True:
                if isinstance(e, commands.CommandInvokeError):
                    await ctx.send(f'[ {ctx.message.content} ] 에서 오류 발생!\n```{e.original}```')
                else:
                    await ctx.send(f'[ {ctx.message.content} ] 에서 오류 발생!\n```{e}```')

    @commands.command(name = '안녕', aliases = ['hello', 'ㅎㅇ'])
    async def 안녕(self, ctx):
        e = discord.Embed(title=f'{ctx.author.display_name}님 안녕하세요!', color = 0xF6F786)
        e.description = ('반가워요 저는 미니봇이에요!\n자세한 설명은 `미니봇 도움`으로 알아보세요!')
        e.set_thumbnail(url=self.bot.user.avatar_url)
        await ctx.send(embed = e)

    @commands.command()
    async def 업타임(self, ctx):
        uptime = round(time.time() - START)
        if uptime >= 86400:
            ut1 = uptime // 86400
            ut2 = uptime % 86400
            ut3 = ut2 // 3600
            ut4 = ut2 % 3600
            ut5 = ut4 // 60
            ut6 = ut4 % 60
            await ctx.send(f'{ut1}일 {ut3}시간 {ut5}분 {ut6}초 동안 작동됨')
        elif uptime >= 3600:
            ut1 = uptime // 3600
            ut2 = uptime % 3600
            ut3 = ut2 // 60
            ut4 = ut2 % 60
            await ctx.send(f'{ut1}시간 {ut3}분 {ut4}초 동안 작동됨')
        elif uptime >= 60:
            ut1 = uptime // 60
            ut2 = uptime % 60
            await ctx.send(f'{ut1}분 {ut2}초 동안 작동됨')
        elif uptime < 60: 
            await ctx.send(f'{uptime}초 동안 작동됨')

    @commands.command()
    async def 초대(self, ctx):
        vote = await reqjson("https://api.koreanbots.cf/bots/get/520830713696878592")
        await ctx.send(embed = discord.Embed(title='미니봇을 다른 서버에 초대해주세요!', description=f'[초대하기](https://discordapp.com/oauth2/authorize?client_id=520830713696878592&scope=bot&permissions=8)\n[Korean Bots](https://koreanbots.cf/bots/520830713696878592) {vote["data"]["votes"]} ❤️').set_footer(text=f'{len(self.bot.guilds)}개의 서버와 함께하는중'))

    @commands.command(name = '도움', aliases = ['help', '도움말'])
    async def 도움(self, ctx):

        e = discord.Embed(title = '미니봇 도움말', description='프리픽스는 **`**, **미니봇**, <@!520830713696878592> 이에요\n 개발자 : `!   "   A Minibox#3466`')
        e.add_field(name = '1페이지', value = '도움말', inline=False)
        e.add_field(name = '2페이지', value = '음악', inline=False)
        e.add_field(name = '3페이지', value = '마이봇', inline=False)
        e.set_footer(text = '[ 1 / 3 ] 이모지로 페이지를 넘길 수 있어요')

        e1 = discord.Embed(title = '미니봇 음악 도움말')
        e1.add_field(name = '미니봇 재생 [검색어]', value = '음악을 재생해요', inline=False)
        e1.add_field(name = '미니봇 나가', value = '통화방에서 나가요', inline=False)
        e1.add_field(name = '미니봇 재생목록', value = '지금 플레이리스트를 보여줘요', inline=False)
        e1.add_field(name = '미니봇 스킵', value = '음악을 하나 스킵해요', inline=False)
        e1.add_field(name = '미니봇 지금곡', value = '지금 플레이중인 곡을 보여줘요', inline=False)
        e1.add_field(name = '미니봇 시간스킵 [초]', value = '초만큼 시간을 스킵해요', inline=False)
        e1.set_footer(text = '[ 2 / 3 ] 이모지로 페이지를 넘길 수 있어요')

        e2 = discord.Embed(title = '미니봇 마이봇 도움말', description = '마이봇은 마이봇을 만든 채널에서**만** 사용 가능해요')
        e2.add_field(name = '미니봇 등록 [웹훅URL]', value = '채널을 DB에다 적용시켜요\n```사용법\n1. 봇을 배치할 채널의 채널 편집에 들어가요\n2. 웹후크칸을 누르고 웹후크 만들기 버튼을 눌러요\n3. 웹후크의 URL을 복사하고 저장하고 명령어에 써요```', inline=False)
        e2.add_field(name = '미니봇 생성 "[봇 이름]" "[프리픽스]"', value = '봇을 만들어요', inline=False)
        e2.add_field(name = '미니봇 커맨드생성 "[봇 이름]" "[커맨드]" "[대답]"', value = '봇의 커맨드를 만들어요', inline=False)
        e2.add_field(name = '미니봇 프사변경 "[봇 이름]" [프사 URL]', value = '봇의 프로필사진을 바꿔요', inline=False)
        e2.add_field(name = '미니봇 봇정보 "[봇 이름]"', value = '봇의 커맨드들과 정보를 보여줘요', inline=False)
        e2.set_footer(text = '[ 3 / 3 ] 이모지로 페이지를 넘길 수 있어요')

        es = [e, e1, e2]
        print(e1.to_dict())
        msg = await ctx.send(embed=e)
        page = Paginator(self.bot, msg, embeds=es, only=ctx.author)
        await page.start()


    @commands.command()
    async def 핑(self,ctx):
        nowasdf = ctx.message.created_at
        try:
            authorcolor = message.author.colour
        except:
            authorcolor = 0x1dc73a
        embed=discord.Embed(title="🏓 핑 !", description="\n", color=authorcolor)
        a = await ctx.send(embed=embed)
        latertime = a.created_at
        ping = latertime - nowasdf
        asdf = str(int(ping.microseconds) / 1000)
        asdf = asdf.split(".")
        asdf = asdf[0]
        embed=discord.Embed(title=f"🏓 퐁!\n메시지 핑 : {asdf}ms\n디스코드 API 핑 : {round(self.bot.latency * 1000)}ms", color=authorcolor)
        await a.edit(embed = embed)

    @commands.command()
    async def 프사(self,ctx, user:discord.Member=None):
        if user == None:
            user = ctx.author
        embed = discord.Embed(title=f'{user.name} 님의 프사')
        embed.set_image(url = user.avatar_url)
        await ctx.send(embed = embed)

    @commands.command()
    async def 저장(self, ctx, *, data):
        id_ = random.randint(1000000000000000, 9999999999999999)
        self.save[id_] = data
        savedata(self.save)
        await ctx.send(f'저장했어요! 코드는 `{id_}` 입니다!')
        await ctx.message.delete()

    @commands.command()
    async def 불러오기(self, ctx, code:int):
        await ctx.author.send(self.save[code])

    @commands.command()
    async def 정보(self, ctx):
        nowasdf = ctx.message.created_at
        msg = await ctx.send(get_emoji(self.bot, 'blueloading'))

        ramstatus = psutil.virtual_memory()
        ramm = str(f"{round((ramstatus[0]/1000000000)-(ramstatus[1]/1000000000), 2)}GB / {round(ramstatus[0]/1000000000, 2)}GB")
        ramm = str(ramm.replace("['", ""))
        ramm = str(ramm.replace("']'", ""))
        cpu = cpuinfo.get_cpu_info()

        latertime = msg.created_at
        ping = latertime - nowasdf
        asdf = str(int(ping.microseconds) / 1000)
        asdf = asdf.split(".")
        asdf = asdf[0]

        embed = discord.Embed(title="미니봇 정보", color = 0x112233)
        embed.add_field(name = "개발자", value = '`!   "   A Minibox#3466`', inline=False)
        embed.add_field(name = "서버 CPU", value = cpu['brand'], inline= False)
        embed.add_field(name = "서버 램", value = ramm)
        embed.add_field(name = "아키텍처", value = cpu["arch"])
        embed.add_field(name = "파이썬 버전", value = cpu['python_version'], inline= False)
        embed.add_field(name = "메시지 핑", value = f"{asdf}ms")
        embed.add_field(name = "디스코드 API 핑", value = f"{round(self.bot.latency * 1000)}ms")

        await msg.edit(embed=embed, content="")

    # @commands.command()
    # async def 마스크(self, msg, *, ji:str):
    #     w = parse.quote(ji)
    #     response = requests.get(f'https://8oi9s0nnth.apigw.ntruss.com/corona19-masks/v1/storesByAddr/json?address={w}', headers={'accept': 'application/json',}).json()
    #     a = str()
    #     a2 = "\n"
    #     a3 = "\n"
    #     b =list()
    #     bbb = list()
    #     for i in response['stores']:
    #         try:
    #             aa = i['remain_stat']
    #             b.append(aa)
    #             if aa == 'empty' or aa == None or aa == 'break':
    #                 pass
    #             else:
    #                 if aa == 'plenty':
    #                     a = f"{a}{i['name']} - {i['stock_at']}\n"
    #                 if aa == 'few':
    #                     a2 = f"{a2}{i['name']} - {i['stock_at']}\n"
    #                 if aa == 'some':
    #                     a3 = f"{a3}{i['name']} - {i['stock_at']}\n"
    #         except KeyError:
    #             pass
    #     if int(len(b)) == 0:
    #         e = discord.Embed(title="이런! 없는 지역이네요!")
    #     elif int(b.count('empty')) + int(b.count(None)) + int(b.count('break')) == int(len(b)):
    #         e = discord.Embed(title=f"이런, {ji} 지역의 모든 약국에서 마스크가 다 팔렸거나 문을 닫았네요..",description=f"전체 : {len(b)}\n다 팔림 : {b.count('empty')}\n정보 없음 : {b.count(None)}\n문 닫음 : {b.count('break')}")
    #     else:
    #         if a == "" or a2 == "\n" or a3 == "\n":
    #             e = discord.Embed(title=f"{response['address']}의 마스크 현황", description=f"전체 : {len(b)}\n다 팔림 : {b.count('empty')}\n정보 없음 : {b.count(None)}\n문 닫음 : {b.count('break')}\n")
    #             e.add_field(name='정보',value=f"많음 :\n{a}\n별로 없음 : \n{a2}\n몇개 밖에 없음 : \n{a3}",inline=False)
    #         else:
    #             e = discord.Embed(title=f"{response['address']}의 마스크 현황", description=f"전체 : {len(b)}\n다 팔림 : {b.count('empty')}\n정보 없음 : {b.count(None)}\n문 닫음 : {b.count('break')}\n")
    #             e.add_field(name='**많음**',value=a,inline=False)
    #             e.add_field(name='**별로 없음**',value=a2,inline=False)
    #             e.add_field(name='**몇개 밖에 없음**',value=a3,inline=False)
    #     await msg.send(embed=e)

def setup (bot) :
    bot.add_cog (Core (bot))
    print ('Core Loaded!')
