import logging
from datetime import datetime
from typing import Set, Tuple

import discord
from discord.ext import commands, tasks
from sqlalchemy import *
from sqlalchemy.orm import Session

from Helix import constants
from Helix.utils.config import Config, ConfigDefaults
from Helix.utils.db_tools import ServerList
from Helix.utils.embed_handler import success, failure

logger = logging.getLogger(__name__)


class Defcon(commands.Cog):
    """
    For protecting against Raids
    """

    def __init__(self, bot, config_file=None):
        if config_file is None:
            config_file = ConfigDefaults.Config_file
        # TODO: setup mysql for defcon data storage for individual servers
        self.config = Config(config_file)
        self.bot = bot
        self.defcon_active = False
        self.sql_host = self.config.sql_host
        self.sql_user = self.config.sql_user
        self.sql_passwd = self.config.sql_passwd
        self.sql_ddb = self.config.sql_ddb

        self.Engine = create_engine(f'mysql+pymysql://{self.sql_user}:{self.sql_passwd}@{self.sql_host}/{self.sql_ddb}',
                                    echo=False)

        self._kicked_while_defcon_was_active: int = 0
        self.joins_per_min_trigger = 7
        self._joins: Set[Tuple[datetime, int]] = set()
        self.staff_channel = bot.get_channel(constants.staff_channel_id)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        # Mitigate latency by using server time
        self._joins.add((datetime.now(), member.id))

        if self.defcon_active:
            await member.kick(
                reason=(
                    "Bot detected mass member join (raid), kicking all new joins for a while.\n"
                    "If you're just a regular user you can wait a bit and try to join later."
                )
            )
            self._kicked_while_defcon_was_active += 1

    @tasks.loop(minutes=1)
    async def mass_join_check(self):
        current_time = datetime.now()

        for join in self._joins.copy():
            if (current_time - join[0]).seconds >= 60:
                self._joins.remove(join)

        with Session(self.Engine) as session:
            serv = ServerList()
            member = self._joins[0]
            Guild = session.query(ServerList).filter_by(ServerID=member.guild.id).first()
            self.joins_per_min_trigger = Guild.DefconThreshold

        if len(self._joins) >= self.joins_per_min_trigger:
            if self.defcon_active:
                return

            self.defcon_active = True
            await self.staff_channel.send(
                f"@here DEFCON activated, detected {len(self._joins)} joins in the last minute!\n"
                f"I'll kick any new joins as long as DEFCON is active, you need to manually disable it with:\n"
                f"H!disable_defcon"
            )

    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def disable_defcon(self, ctx):
        self.defcon_active = False
        await ctx.send(embed=success(
            f"Successfully deactivated DEFCON.\n"
            f"Kicked user count: {self._kicked_while_defcon_was_active}"
        )
        )
        self._kicked_while_defcon_was_active = 0

    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def set_defcon_trigger(self, ctx, trigger: int):
        if not 7 <= trigger <= 100:
            return await ctx.send(embed=failure("Please use integer from 7 to 100."))

        self.joins_per_min_trigger = trigger
        await ctx.send(embed=success(f"Successfully changed DEFCON trigger to {trigger} users/min."))


def setup(bot):
    bot.add_cog(Defcon(bot))
