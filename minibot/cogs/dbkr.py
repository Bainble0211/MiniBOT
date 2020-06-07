import dbkrpy
import discord
from discord.ext import commands
import aiohttp

async def req (url : str, header = None) :
   async with aiohttp.ClientSession () as session:
      async with session.get (url = url, headers=header) as r :
         data = await r.json()
   return data

async def post_guild_count(token, guild_count):
    URL = 'https://api.koreanbots.cf/bots/servers'
    headers = {"token":token,"content-type":"application/json"}
    data = {'servers':guild_count}
    async with aiohttp.ClientSession() as cs:
        async with cs.post(URL, headers=headers, json=data) as r:
            response = await r.json()
            return response

class UpdateGuild(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.token = 'DBKR TOKEN'
        dbkrpy.UpdateGuilds(bot,self.token)

    @commands.command(name = '확인')
    async def 확인(self, ctx, user:discord.User = None):
        if user == None:
            user = ctx.author
        data = await req(url= f"https://api.koreanbots.cf/bots/voted/{user.id}", header={"token":self.token,"content-type":"application/json"})
        vote = await req("https://api.koreanbots.cf/bots/get/520830713696878592")
        if data['code'] == 200:
            if data["voted"] == True:
                await ctx.send(embed = discord.Embed(description = f'{user}님 투표해주셔서 감사해요! [투표하기](https://koreanbots.cf/bots/520830713696878592) {vote["data"]["votes"]} ❤️'))
            else:
                await ctx.send(embed = discord.Embed(description = f'{user}님은 투표를 안했네요 투표해주세요!!! [투표하기](https://koreanbots.cf/bots/520830713696878592) {vote["data"]["votes"]} ❤️'))
        else:
            await ctx.send(embed = discord.Embed(description = f'{user}님은 투표를 안했네요 투표해주세요!!! [투표하기](https://koreanbots.cf/bots/520830713696878592) {vote["data"]["votes"]} ❤️'))
    
    @commands.command()
    async def 순위(self, ctx):
        data = await req(f'https://api.koreanbots.cf/bots/get')
        a = str()
        n = 1
        for i in data['data']:
            a += f"{n}위 - {i['name']} : {i['servers']}서버 {i['votes']} ❤️\n"
            n += 1
        await ctx.send(a)

    @commands.command()
    async def 서버수(self, ctx, token, gu):
        d = await post_guild_count(token, gu)
        await ctx.send(d)

def setup(bot):
    bot.add_cog(UpdateGuild(bot))