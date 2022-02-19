from discord.ext.commands import Cog
from discord_slash.cog_ext import cog_slash
from commands.SlashProfile import SlashProfile
from util.constants import serverid
from db.local_db import server


class Profile(Cog):

    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("help")

    @cog_slash(name="profile", guild_ids=[serverid])
    async def profile_slash(self, ctx):
        if ctx.channel.id not in [server.robot_channel.id, 883616650711138354] or ctx.author != 510105779274121216:
            await ctx.reply(f"Please use bot commands in <#{server.robot_channel.id}> .", delete_after=30)
            return
        response = SlashProfile(ctx)
        await response.run()


def setup(bot):
    bot.add_cog(Profile(bot))
