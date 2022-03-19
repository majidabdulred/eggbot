import signal
from discord import Message, Intents
from discord_slash import SlashCommand
from discord.ext.commands import Bot as BotBase
from os import getenv
from dotenv import load_dotenv
from util import mylogs
from util import constants as C
from util.handle_errors import handle_errors
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from cogs.results import handle_component

PREFIX = "!"
load_dotenv()
TOKEN = getenv(C.env_name)


class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.scheduler = AsyncIOScheduler()
        self.server = None
        intents = Intents(guilds=True, members=True, messages=True)
        super().__init__(command_prefix=PREFIX, intents=intents)

    def setup(self):
        self.load_extension(f"cogs.commands")
        self.load_extension(f"cogs.initialise")
        self.load_extension(f"cogs.verify")
        self.load_extension(f"cogs.token")
        self.load_extension(f"cogs.profile")
        self.load_extension(f"cogs.race")
        mylogs.info("COGS_LOADED")

    def run(self):
        mylogs.info("Running Setup ....")
        self.setup()

        super().run(TOKEN, reconnect=True)

    async def on_command_error(self, context, exc):
        await handle_errors(exc, context)

    async def on_slash_command_error(self, ctx, exc):
        await handle_errors(exc, ctx)

    async def on_component_callback_error(self, ctx, ex):
        await handle_errors(ex, ctx)

    async def on_message(self, message: Message):
        if message.author != self.user:
            ctx = await self.get_context(message)
            if ctx.valid:
                await self.invoke(ctx)

    async def on_component(self, ctx):
        if ctx.custom_id.startswith("results_chickens_"):
            await handle_component(ctx)

    async def on_ready(self):
        self.data_channel = self.get_channel(C.data_channel)
        self.error_channel = self.get_channel(C.error_channel)
        if not self.ready:
            try:
                self.loop.add_signal_handler(getattr(signal, 'SIGINT'),
                                             lambda: self.loop.create_task(self.signal_handler()))
                self.loop.add_signal_handler(getattr(signal, 'SIGTERM'),
                                             lambda: self.loop.create_task(self.signal_handler()))
            except NotImplementedError:
                mylogs.warning("Signal handlers not added")
            self.ready = True

        else:
            mylogs.warning("Bot reconnecting....")
        mylogs.info("Ready")

    async def signal_handler(self):
        mylogs.critical("Time to say good bye")
        await self.close()

    async def on_connect(self):
        mylogs.info("BOT_CONNECTED")

    async def on_disconnect(self):
        mylogs.warning("BOT_DISCONNECTED")


bot = Bot()
slash = SlashCommand(bot, sync_commands=True)
bot.run()
