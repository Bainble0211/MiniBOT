import discord, time
from discord.ext import commands
from config import TOKEN, EXTENSIONS

START = time.time()

class MiniBOT (commands.Bot) : 
    def __init__ (self) :
        super().__init__ (
            command_prefix=["`", "미니봇 ", "<@!520830713696878592> ","미니봇","<@!520830713696878592>"]
        )
        self.remove_command("help")

        for i in EXTENSIONS :
            self.load_extension (i)
    
    async def on_ready (self) :
        print (f'{self.user.name} 준비 완료!')
    
    async def on_message (self, message) :
        if message.author.bot :
            return
        else :
            await self.process_commands (message)

bot = MiniBOT ()
bot.run (TOKEN, bot=True)
