# Name Helix
from datetime import datetime, timedelta

import aiohttp
import discord
import sentry_sdk
import yaml
from discord.ext import commands
from sqlalchemy import *
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database

from Helix.utils.db_tools import ServerList, Users, Stats, Config, BlackList, Mutes

# Sentry error reporting
sentry_sdk.init(
    "https://fe349234191e4e86a83c8cd381068ab4@o901570.ingest.sentry.io/5994911",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)

# Discord Intents
intents = discord.Intents.default()
intents.typing = True
intents.presences = True
intents.members = True
intents.messages = True
guild_subscriptions = True
fetch_offline_members = True

bot = commands.AutoShardedBot


class Helix(bot):
    def __init__(self):
        self.description = """
                Helix - A Custom Bot for SinLess Games Official Discord Server and more!
                """

        # Opens the config and reads it, no need for changes unless you'd like to change the library (no need to do so unless
        # having issues with ruamel)
        with open("Helix/Configs/config.yml", "r", encoding="utf-8") as file:
            self.config = yaml.safe_load(file)

        # Config Variables
        self.TOKEN = self.config['Token']
        self.VERSION = self.config['Version']
        self.OWNER_ID = self.config['bot_owner_id']
        self.prefix = self.config['DefaultPrefix']
        self.sql_host = self.config['SQL_Host']
        self.sql_user = self.config['SQL_UserName']
        self.sql_passwd = self.config['SQL_Password']
        self.sql_ddb = self.config['DefaultDatabase']

        super().__init__(
            command_prefix=self.prefix,
            intents=intents,
            description=self.description,
            ase_insensitive=True,
            start_time=datetime.utcnow(),
        )
        super().remove_command('help')

        # SqlAlchemy engine construction
        self.sql_engine = create_engine(
            f'mysql+pymysql://{self.sql_user}:{self.sql_passwd}@{self.sql_host}/{self.sql_ddb}', echo=False)
        if not database_exists(self.sql_engine.url):
            create_database(self.sql_engine.url)
        else:
            # If DB exists prints database_exists
            print(database_exists(self.sql_engine.url))

    async def load(self, ctx, extention):
        self.load_extension(f'./Helix/cogs/{extention}')

    async def unload(self, ctx, extention):
        self.unload_extension(f'./Helix/cogs/{extention}')

    def run(self):

        print("Running bot...")
        super().run(self.TOKEN, reconnect=True)

    async def shutdown(self):
        print("Closing connection to Discord...")
        await super().close()

    async def close(self):
        print("Closing on keyboard interrupt...")
        await self.shutdown()

    async def on_connect(self):
        self.session = aiohttp.ClientSession(loop=self.loop)

        cT = datetime.now() + timedelta(
            hours=5, minutes=30
        )  # GMT+05:30 is Our TimeZone So.

        print(
            f"[ Log ] {self.user} Connected at {cT.hour}:{cT.minute}:{cT.second} / {cT.day}-{cT.month}-{cT.year}"
        )

    async def on_resumed(self):
        print("Bot resumed.")

    async def on_disconnect(self):
        print("Bot disconnected.")

    async def on_error(self, err, *args, **kwargs):
        raise

    async def on_command_error(self, ctx, exc):
        raise getattr(exc, "original", exc)

    async def on_ready(self):
        cT = datetime.now() + timedelta(
            hours=5, minutes=30
        )  # GMT+05:30 is Our TimeZone So.

        print(
            f"[ Log ] {self.user} Ready at {cT.hour}:{cT.minute}:{cT.second} / {cT.day}-{cT.month}-{cT.year}"
        )
        print(f"[ Log ] GateWay WebSocket Latency: {self.latency * 1000:.1f} ms")
        self.client_id = (await self.application_info()).id
        print(f'\033[1;32m Bot is ready! DEUS VULT!')

        config_activity = self.config['bot_activity']
        activity = discord.Game(name=self.config['bot_status_text'])

        await self.change_presence(status=config_activity, activity=activity)

        async for guild in self.fetch_guilds():
            memberList = []
            channelList = await guild.fetch_channels()
            async for member in guild.fetch_members():
                memberList.append(member)
            members = len(memberList)
            # print("members: " + str(members))
            channels = len(channelList)
            # print("channels: " + str(channels))

            ServerList.__table__.create(bind=self.sql_engine, checkfirst=True)

            # create server specific databases
            with Session(self.sql_engine) as session:
                serv = ServerList()

                GuildExists = session.query(ServerList).filter_by(ServerID=guild.id).first()
                if not GuildExists:
                    serv.ServerID = guild.id
                    serv.ServerName = guild.name
                    serv.MemberCount = members
                    serv.ChannelCount = channels
                    serv.LastUpdate = datetime.now()
                    session.add(serv)
                    session.commit()
                    session.close()

                else:
                    session.query(ServerList).filter_by(ServerID=guild.id).update({
                        "ServerName": guild.id,
                        "MemberCount": members,
                        "ChannelCount": channels,
                        "LastUpdate": datetime.now()
                    }, synchronize_session="fetch")
                    session.commit()
                    session.close()

        async for guild in self.fetch_guilds():
            Engine = create_engine(f'mysql+pymysql://{self.sql_user}:{self.sql_passwd}@{self.sql_host}/{guild.id}',
                                   echo=False)
            if not database_exists(Engine.url):
                create_database(Engine.url)
            else:
                # If DB exists prints database_exists
                print(database_exists(Engine.url))

            usr = Users()
            sts = Stats()
            cfg = Config()
            bl = BlackList()
            mut = Mutes()

            Users.__table__.create(bind=Engine, checkfirst=True)
            Stats.__table__.create(bind=Engine, checkfirst=True)
            Config.__table__.create(bind=Engine, checkfirst=True)
            BlackList.__table__.create(bind=Engine, checkfirst=True)
            Mutes.__table__.create(bind=Engine, checkfirst=True)

            with Session(Engine) as session:
                pass

    async def process_commands(self, msg):
        ctx = await self.get_context(msg, cls=commands.Context)

        if ctx.command is not None:
            await self.invoke(ctx)

    async def on_message(self, msg):
        if not msg.author.bot:
            await self.process_commands(msg)


bot = Helix()
