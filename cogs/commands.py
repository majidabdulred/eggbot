"""
For !token , !makegif , !me commands.
"""
from io import BytesIO

import imageio
from aiohttp import request
from discord import File
from discord.ext.commands import Cog, command, cooldown, BucketType
from discord_slash import ButtonStyle
from discord_slash.cog_ext import cog_slash
from discord_slash.utils.manage_components import create_button, create_actionrow

import util.slash_options as op
from db.chickens import get_chicken, get_many_chickens
from util import create_embeds, mylogs
import util.constants as C




class Makegif(Cog):

    def __init__(self, bot):
        self.bot = bot

    @command(name="gif", aliases=["makegif"])
    @cooldown(20, 60, BucketType.guild)
    async def makegif(self, ctx, *args):
        mylogs.debug(f"COMMAND_USED : gif :{ctx.author.name} : {args}")
        tokens, message = self._convert_args_to_token(args)
        if tokens is None:
            await ctx.reply(message)
            return
        wait = await ctx.reply("Making your lovely gif....")
        file = await self._gifmake(tokens)
        if file is None:
            await wait.delete()
            await ctx.reply("Something Went Wrong")
            return
        gif = BytesIO()
        gif.write(file)
        gif.seek(0)
        await wait.delete()
        await ctx.reply(content=message, file=File(gif, filename="result.gif"))
        gif.close()

    def _convert_args_to_token(self, args):
        """Returns a list containing valid token number and a message of invalid token numbers"""
        invalid = []
        message = ""
        tokennums = []
        for tok in args:
            if not tok.isdigit():
                invalid.append(tok)
                continue
            elif 1 <= int(tok) <= 33333:
                tokennums.append(int(tok))
            else:
                invalid.append(tok)
        if len(invalid) > 0:
            message += f"\nInvalid token ids : {invalid}"
        if not 1 < len(tokennums) <= 10:
            message += f"\nPlease enter between 2 to 10 token ids."
            return None, message
        return tokennums, message

    async def _gifmake(self, tokens):
        """Queries image url , downloads the image and makes the actual gif"""
        err = 0
        chicks = await get_many_chickens(tokens)
        urls = [ur["image_url"] for ur in chicks]
        images = []
        for url in urls:
            img = await self._download_image(url)
            if img is not None:
                images.append(img)
            else:
                mylogs.warning(f"Image not found {url}")
                err += 1
                continue
        if err > 0:
            mylogs.warning(f"Images not found : Amount = {err}")
        if len(images) >= 2:
            return imageio.mimwrite('<bytes>', images, ".gif", fps=2)

    async def _download_image(self, url):
        """Downloads the image and returns the binary text"""
        image_url = url
        filename = image_url.split("/")[-1].split("?")[0]
        async with request("GET", image_url) as re:
            if re.status == 200:
                con = await re.read()
                mylogs.info(f'Downloaded: + {filename}')
                im = imageio.imread(con, ".png")
                return im
            else:
                mylogs.error(str(await re.text()))


def setup(bot):
    bot.add_cog(Makegif(bot))
