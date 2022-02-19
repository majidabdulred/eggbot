import asyncio

from discord.ext.commands import Bot as BotBase
from discord import Intents
from os import getenv
from discord_slash import SlashCommand
from dotenv import load_dotenv
from util.handle_errors import handle_errors
from db.local_db import server

PREFIX = "!"
load_dotenv()


class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        intents = Intents(guilds=True, members=True, messages=True)
        super().__init__(command_prefix=PREFIX, intents=intents)

    def run(self):
        self.load_extension(f"cogs.commands")
        self.load_extension(f"cogs.initialise")
        self.load_extension(f"cogs.verify")
        self.load_extension(f"cogs.profile")

        super().run(getenv("TEST"), reconnect=True)

    async def on_slash_command_error(self, ctx, exc):
        await handle_errors(exc, ctx)

    async def on_message(self, message):
        if message.author != self.user:
            ctx = await self.get_context(message)
            if ctx.valid:
                await self.invoke(ctx)

    async def on_component_callback_error(self, ctx, ex):
        print("COMP ERROR")

    async def on_ready(self):
        server.__setattr__("guild", await self.fetch_guild(936169787724275732))
        print("Ready")


bot = Bot()
slash = SlashCommand(bot, sync_commands=True)

bot.run()
