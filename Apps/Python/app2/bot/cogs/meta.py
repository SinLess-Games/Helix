from datetime import datetime, timedelta
from platform import python_version
from time import time

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord import Activity, ActivityType, Embed
from discord import __version__ as discord_version
from discord.ext.commands import Cog
from discord.ext.commands import command
from psutil import Process, virtual_memory
import yaml


class Meta(Cog):
    def __init__(self, client):
        self.client = client

        scheduler = AsyncIOScheduler()

        self._message = "watching +help | {users:,} users in {guilds:,} servers"

        scheduler.add_job(self.set, CronTrigger(second=0))

    @property
    def message(self):
        return self._message.format(users=len(self.client.users), guilds=len(self.client.guilds))

    @message.setter
    def message(self, value):
        if value.split(" ")[0] not in ("playing", "watching", "listening", "streaming"):
            raise ValueError("Invalid activity type.")

        self._message = value

    async def set(self):
        _type, _name = self.message.split(" ", maxsplit=1)

        await self.client.change_presence(activity=Activity(
            name=_name, type=getattr(ActivityType, _type, ActivityType.playing)
        ))

    @command(name="set activity")
    async def activity(self, ctx, *, text: str):
        self.message = text
        await self.set()

    @command(name="ping")
    async def ping(self, ctx):
        start = time()
        message = await ctx.send(f"Pong! DWSP latency: {self.client.latency * 1000:,.0f} ms.")
        end = time()

        await message.edit(
            content=f"Pong! DWSP latency: {self.client.latency * 1000:,.0f} ms. Response time: {(end - start) * 1000:,.0f} ms.")

    @command(name="stats1")
    async def stats1(self, ctx):
        embed = Embed(title="HELIX stats",
                      colour=ctx.author.colour,
                      thumbnail=self.client.user.avatar_url,
                      timestamp=datetime.utcnow())

        proc = Process()
        with proc.oneshot():
            uptime = timedelta(seconds=time() - proc.create_time())
            cpu_time = timedelta(seconds=(cpu := proc.cpu_times()).system + cpu.user)
            mem_total = virtual_memory().total / (1024 ** 2)
            mem_of_total = proc.memory_percent()
            mem_usage = mem_total * (mem_of_total / 100)

        with open("config.yml", 'r') as i:
            cfg = yaml.safe_load(i)

        VERSION = cfg['Helix_BOT']['Version']

        fields = [
            ("Bot version", VERSION, True),
            ("Python version", python_version(), True),
            ("discord.py version", discord_version, True),
            ("Uptime", uptime, True),
            ("CPU time", cpu_time, True),
            ("Memory usage", f"{mem_usage:,.3f} / {mem_total:,.0f} MiB ({mem_of_total:.0f}%)", True)
        ]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Meta(client))
