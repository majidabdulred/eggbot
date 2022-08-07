from pandas.core.indexing import IndexingError

from util import mylogs

from discord.errors import HTTPException, Forbidden,NotFound
from discord.ext.commands import CommandNotFound, BadArgument, MissingRequiredArgument, BadBoolArgument, \
    CommandOnCooldown
from discord_slash.error import IncorrectFormat
from datetime import timedelta
from asyncio.exceptions import TimeoutError


def updateCheck(res, msg):
    if res.acknowledged and res.modified_count >= 1 and res.matched_count >= 1:
        mylogs.info(f"DB_SUCCESS : {msg}")
        return
    if not res.acknowledged:
        mylogs.warning(f"DB_ACK_FAILED : {msg}")
    if res.matched_count < 1:
        mylogs.warning(f"DB_NOT_FOUND : {msg}")
    if res.modified_count < 1:
        mylogs.info(f"DB_ALREADY_UPDATES: {msg}")


def timeconvert(sec):
    timelist = str(timedelta(seconds=sec)).split(":")
    hrs = timelist[0].lstrip('0') + ' hrs'
    mins = timelist[1].lstrip('0') + ' mins'
    secs = timelist[2].split('.')[0].lstrip('0') + ' sec'
    if 60 > sec:
        return secs
    if 60 <= sec < 3600:
        return f"{mins} {secs.lstrip(' sec')}".strip()
    elif sec >= 3600:
        return f"{hrs} {mins.lstrip(' mins')}".strip()


async def handle_errors(exc, ctx):
    if hasattr(exc, "original"):
        error = exc.original
    else:
        error = exc
    if isinstance(error, TimeoutError):
        # comps = ctx.message.components
        # comps[0]["components"] = [button for button in comps[0]["components"] if "url" in button.keys()]
        try:
            await ctx.message.edit(components=[])
        except AttributeError:
            mylogs.debug("CTX_MESSAGE_NOT_FOUND")
        mylogs.debug(f"TIMEOUT : {ctx.message.id}")
    elif isinstance(error,NotFound):
        mylogs.error("INTERACTION_NOT_FOUND")
    elif isinstance(error,ValueError):
        pass
    else:
        raise error


async def old_handle_errors(exc, ctx):
    if hasattr(exc, "original"):
        Error = exc.original
    else:
        Error = exc
    if isinstance(Error, AttributeError) and "'SlashContext' object has no attribute 'reply'" in Error.args:
        return
    if isinstance(Error, CommandNotFound):
        return

    mylogs.warning(f"{ctx.author.name} {exc}")
    if any([isinstance(Error, error) for error in (MissingRequiredArgument, BadBoolArgument, BadArgument)]):
        await ctx.send("Command not used properly.")

    elif any([isinstance(Error, error) for error in (CommandNotFound, HTTPException)]):
        pass

    elif isinstance(Error, CommandOnCooldown):
        # await ctx.reply(
        #     f"This command is limited to **1 use** per **{timeconvert(Error.cooldown.per)}**. "
        #     f"Try again after **{timeconvert(Error.retry_after)}**.")
        mylogs.warning("More than 20 req in last 1 min.")
    elif isinstance(Error, Forbidden):
        await ctx.send("Don't have permissions")

    elif isinstance(Error, ValueError):
        if Error.args[0] == "OpenseaApiError":
            await ctx.send("Wrong Address")
        elif Error.args[0] == "LenAddress":
            await ctx.send("Wrong address")

    elif isinstance(Error, IndexingError):
        await ctx.send("Please see pinned messages on how to use this command.")

    elif isinstance(Error, IncorrectFormat):
        pass
    else:
        raise Error
