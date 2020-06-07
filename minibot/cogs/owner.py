import discord
import ast
import asyncio
import subprocess
from discord.ext import commands
from config import OWNERS
from config import EXTENSIONS

def insert_returns(body):
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)

def is_owner():
    async def predicate(ctx):
        return ctx.author.id in OWNERS
    return commands.check(predicate)

class Owners (commands.Cog) :
    def __init__ (self, bot) :
        self.bot = bot
        self.normal_color = 0x00fa6c
        self.error_color = 0xff4a4a

    @commands.Cog.listener()
    async def on_command_error(self, ctx, e):
        if str(type(e)) == "<class 'discord.ext.commands.errors.CheckFailure'>":
            pass

    @commands.command(name = 'reload', aliases = ['리로드','r'])
    @is_owner()
    async def 리로드(self, ctx, c=None):
        if c == None:
            try:
                for i in EXTENSIONS :
                    self.bot.reload_extension (i)
                await ctx.send(f"모든 모듈을 리로드했어요.")
            except Exception as a:
                await ctx.send(f"리로드에 실패했어요. [{a}]")
        else:
            try:
                self.bot.reload_extension(c)
                await ctx.send(f"{c} 모듈을 리로드했어요.")
            except Exception as a:
                await ctx.send(f"{c} 모듈 리로드에 실패했어요. [{a}]")

    @commands.command(name = 'eval')
    @is_owner()
    async def eval_fn(self, ctx, *, cmd):
        try:
            fn_name = "_eval_expr"
            cmd = cmd.strip("` ")
            cmd = "\n".join(f"    {i}" for i in cmd.splitlines())
            body = f"async def {fn_name}():\n{cmd}"
            parsed = ast.parse(body)
            body = parsed.body[0].body
            insert_returns(body)
            env = {
                'bot': self.bot,
                'discord': discord,
                'commands': commands,
                'ctx': ctx,
                '__import__': __import__
                }
            exec(compile(parsed, filename="<ast>", mode="exec"), env)

            result = (await eval(f"{fn_name}()", env))
            await ctx.send(result)
        except Exception as a:
            await ctx.send(a)

    @commands.command(name = 'sudo')
    async def sudo(self, ctx, *, cmd):
        if ctx.author.id == 310247242546151434:
            cmds = cmd.split(' ')
            if cmds[0] == 'eval':
                await self.eval_fn(ctx = ctx, cmd = cmds[1])
            elif cmds[0] == '리로드':
                await self.리로드(ctx = ctx)

    @commands.command ()
    @is_owner()
    async def shell (self, ctx, *cmd) :
        try :
            cmd = " ".join(cmd[:])
            res = subprocess.check_output(cmd, shell=True, encoding='utf-8')
            embed=discord.Embed(title="**Command Sent!**", description=f"Input : **{cmd}**", color=self.normal_color)
            embed.add_field(name="Output", value=f"```{res}```")
            await ctx.send(embed=embed)
        except (discord.errors.HTTPException) :
            await ctx.send ('글자수가 많아 일반 텍스트로 전송합니다.')
            cmd = " ".join(cmd[:])
            res = subprocess.check_output(cmd, shell=True, encoding='utf-8')
            await ctx.send("```" + res + "```")
        except (subprocess.CalledProcessError) :
            embed=discord.Embed(title="**Command Error!**", description="명령어 처리 도중 오류 발생!",color=self.error_color)
            await ctx.send(embed=embed)

def setup (bot) :
    bot.add_cog (Owners (bot))
    print ('Owners Loaded!')
