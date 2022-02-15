import asyncio

from discord.ext.commands import Bot as BotBase
from discord import Intents
from os import getenv
from discord_slash import SlashCommand
from dotenv import load_dotenv

PREFIX = "!"
load_dotenv()


class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        intents = Intents.all()
        super().__init__(command_prefix=PREFIX, intents=intents)

    def run(self):
        self.load_extension(f"cogs.testcog")

        super().run(getenv("TEST"), reconnect=True)

    async def on_ready(self):
        self.server = self.get_guild(936169787724275732)
        print("Ready")

bot = Bot()
bot.run()
