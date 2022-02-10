import signal
from discord import Message, Intents
from discord_slash import SlashCommand
from discord.ext.commands import Bot as BotBase
from os import getenv
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from util import mylogs
from util import constants as C
PREFIX = "!"
load_dotenv()
TOKEN = getenv(C.env_name)

class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.scheduler = AsyncIOScheduler()
        self.server = None
        intents = Intents.all()
        super().__init__(command_prefix=PREFIX, intents=intents)

    def setup(self):
        self.load_extension(f"cogs.initialise")
        self.load_extension(f"cogs.commands")
        # self.load_extension(f"cogs.find")
        self.load_extension(f"cogs.verify")
        mylogs.info("Cogs loaded.")

    def run(self):
        mylogs.info("Running Setup")
        self.setup()

        super().run(TOKEN, reconnect=True)

    # async def on_command_error(self, context, exc):
    #     await handle_errors(exc, context)
    #
    # async def on_slash_command_error(self, ctx, exc):
    #     await handle_errors(exc, ctx)
    #
    # async def on_component_callback_error(self, ctx, ex):
    #     await handle_errors(ex, ctx)

    async def on_message(self, message: Message):
        if message.author != self.user:
            ctx = await self.get_context(message)
            if ctx.valid:
                await self.invoke(ctx)

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
        mylogs.info("Bot Connected")

    async def on_disconnect(self):
        mylogs.warning("Bot Disconnected")


bot = Bot()
slash = SlashCommand(bot, sync_commands=True)
bot.run()
