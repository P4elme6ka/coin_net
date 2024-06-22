from discord.ext import commands
import discord
from config import settings


class MyBot(commands.Bot):

    def __init__(self, command_prefix, self_bot):
        commands.Bot.__init__(self, command_prefix=command_prefix, self_bot=self_bot, intents=discord.Intents.default())
        self.message1 = "[INFO]: Bot now online"
        self.message2 = "Bot still online"
        self.add_commands()

    async def on_ready(self):
        print(self.message1)

    def add_commands(self):
        @self.command(name="status", pass_context=True)
        async def status(ctx):
            await ctx.send(self.message2)


bot = MyBot(command_prefix="!", self_bot=False)
bot.run(settings['token'])
