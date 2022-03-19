import asyncio

from discord.ext.commands import Bot as BotBase
from discord import Intents
from os import getenv
from discord_slash import SlashCommand
from dotenv import load_dotenv
# from util.handle_errors import handle_errors
from tasks.results import scheduler_race_results
from util import handle_errors
from cogs.results import handle_component

PREFIX = "!"
load_dotenv()


class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        intents = Intents.none()
        super().__init__(command_prefix=PREFIX, intents=intents)

    def run(self):
        self.load_extension("cogs.token")
        print("cogs loaded")
        super().run(getenv("TEST"), reconnect=True)

    #
    # async def on_slash_command_error(self, ctx, exc):
    #     await handle_errors(exc, ctx)

    # async def on_message(self, message):
    #     if message.author != self.user:
    #         ctx = await self.get_context(message)
    #         if ctx.valid:
    #             await self.invoke(ctx)
    # #
    # async def on_component_callback_error(self, ctx, ex):
    #     print("COMP ERROR")
    async def on_component(self, ctx):
        if ctx.custom_id.startswith("results_chickens_"):
            await handle_component(ctx)

    async def on_ready(self):
        print("Ready")
        # server.__setattr__("guild", await self.fetch_guild(936169787724275732))
        # await self.wait_until_ready()
        # loop = asyncio.get_event_loop()
        # await asyncio.sleep(10)
        # if not self.ready:
        #     loop.create_task(scheduler_race_results(10))


bot = Bot()
slash = SlashCommand(bot, sync_commands=True)
bot.run()
