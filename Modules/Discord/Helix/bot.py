# Name Helix

import asyncio
import logging
import sys
import time
from collections import defaultdict
from datetime import datetime, timedelta
from functools import wraps

import aiohttp
import colorlog
import discord
import sentry_sdk
from discord.ext import commands
from sqlalchemy import *
from sqlalchemy_utils import database_exists, create_database

from Helix.spotify import Spotify
from Helix.util import load_file
from Helix.utils import exceptions
from Helix.utils.config import Config, ConfigDefaults
from Helix.utils.db_tools import Users, Stats, BlackList, Mutes, ServConfig, ServerList, Bans, Bots
from Helix.utils.opus_loader import load_opus_lib

# Load opus library
load_opus_lib()

# Initialize log
log = logging.getLogger(__name__)


# class construction for Helix Bot base
class Helix(commands.AutoShardedBot):
    # Helix bot Initialize
    def __init__(self, config_file=None):

        # sets descriptions
        global tsr
        if config_file is None:
            config_file = ConfigDefaults.Config_file

        self.description = """
        Helix - A Custom Bot for SinLess Games Official Discord Server and more!
        """

        self.config = Config(config_file)

        def debug_lvl():
            # Checks Debug setting
            if str(self.config.debug_level) == 'CRITICAL':
                sen_level = 0.2
                return sen_level
            elif str(self.config.debug_level) == 'WARNING':
                sen_level = .5
                return sen_level
            elif str(self.config.debug_level) == 'DEBUG':
                sen_level = 1.0
                return sen_level

        # Sentry error reporting
        sentry_sdk.init(
            "https://fe349234191e4e86a83c8cd381068ab4@o901570.ingest.sentry.io/5994911",

            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for performance monitoring.
            # We recommend adjusting this value in production.
            traces_sample_rate=debug_lvl()
        )

        # Config Variables
        self.TOKEN = self.config.login_token
        self.VERSION = self.config.version
        self.OWNER_ID = self.config.owner_id
        self.prefix = self.config.prefix
        self.sql_host = self.config.sql_host
        self.sql_user = self.config.sql_user
        self.sql_passwd = self.config.sql_passwd
        self.sql_ddb = self.config.sql_ddb

        self.exit_signal = None
        self.init_ok = False
        self.cached_app_info = None
        self.last_status = None

        # logging setup
        self._setup_logging()

        # Auto Playlist file loader
        self.auto_playlist = load_file(self.config.auto_playlist_file)
        if not self.auto_playlist:
            log.warning("Auto playlist is empty, disabling.")
            self.config.auto_playlist = False
        else:
            log.info("Loaded auto playlist with {} entries".format(len(self.auto_playlist)))

        # aio lock
        self.aio_Locks = defaultdict(asyncio.Lock)
        log.info('Starting MusicBot {}'.format(self.VERSION))

        # If auto playlist does not exist
        if not self.auto_playlist:
            log.warning("Auto playlist is empty, disabling.")
            self.config.auto_playlist = False

        # else loads playlist
        else:
            log.info("Loaded auto playlist with {} entries".format(len(self.auto_playlist)))

        # TODO: Do these properly
        ssd_defaults = {
            'last_np_msg': None,
            'auto_paused': False,
            'availability_paused': False
        }
        self.server_specific_data = defaultdict(ssd_defaults.copy)

        # Discord Intents
        intents = discord.Intents.all()

        # Super initialize (sets prefix, intents, description, case sensitivity, and start time
        super().__init__(
            command_prefix=self.prefix,
            intents=intents,
            description=self.description,
            case_insensitive=True,
            start_time=datetime.utcnow(),
        )
        # removes help command
        super().remove_command('help')

        # Starts aio session
        self.aio_session = aiohttp.ClientSession(loop=self.loop)
        self.http.user_agent += ' Helix BOT/%s' % self.VERSION

        # Spotify setup
        self.spotify = None
        if self.config.spotify:
            try:
                self.spotify = Spotify(self.config.spotify_clientid, self.config.spotify_clientsecret,
                                       aiosession=self.aio_session, loop=self.loop)
                if not self.spotify.token:
                    log.warning('Spotify did not provide us with a token. Disabling.')
                    self.config._spotify = False
                else:
                    log.info('Authenticated with Spotify successfully using client ID and secret.')
            except exceptions.SpotifyError as e:
                log.warning(
                    'There was a problem initialising the connection to Spotify. Is your client ID and secret correct? Details: {0}. Continuing anyway in 5 seconds...'.format(
                        e))
                self.config._spotify = False
                time.sleep(5)  # make sure they see the problem

        # SqlAlchemy engine construction
        self.sql_engine = create_engine(
            f'mysql+pymysql://{self.sql_user}:{self.sql_passwd}@{self.sql_host}/{self.sql_ddb}', echo=False)
        if not database_exists(self.sql_engine.url):
            create_database(self.sql_engine.url)
        else:
            # If DB exists prints database_exists
            print(database_exists(self.sql_engine.url))

    # Logging set up function
    def _setup_logging(self):
        if len(logging.getLogger(__package__).handlers) > 1:
            logging.debug("Skipping logger setup, already set up")
            return

        # Sets Log format
        s_handler = logging.StreamHandler(stream=sys.stdout)
        s_handler.setFormatter(colorlog.LevelFormatter(
            fmt={
                'DEBUG': '{log_color}[{levelname}:{module}] {message}',
                'INFO': '{log_color}{message}',
                'WARNING': '{log_color}{levelname}: {message}',
                'ERROR': '{log_color}[{levelname}:{module}] {message}',
                'CRITICAL': '{log_color}[{levelname}:{module}] {message}',

                'EVERYTHING': '{log_color}[{levelname}:{module}] {message}',
                'NOISY': '{log_color}[{levelname}:{module}] {message}',
                'VOICEDEBUG': '{log_color}[{levelname}:{module}][{relativeCreated:.9f}] {message}',
                'FFMPEG': '{log_color}[{levelname}:{module}][{relativeCreated:.9f}] {message}'
            },
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'white',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',

                'EVERYTHING': 'white',
                'NOISY': 'white',
                'FFMPEG': 'bold_purple',
                'VOICEDEBUG': 'purple',
            },
            style='{',
            datefmt=''
        ))
        s_handler.setLevel(self.config.debug_level)
        logging.getLogger(__package__).addHandler(s_handler)

        logging.debug("Set logging level to {}".format(self.config.debug_level_str))

        if self.config.debug_mode == 'debug':
            d_logger = logging.getLogger('discord')
            d_logger.setLevel(logging.DEBUG)
            d_handler = logging.FileHandler(filename='logs/discord.log', encoding='utf-8', mode='w')
            d_handler.setFormatter(logging.Formatter('{asctime}:{levelname}:{name}: {message}', style='{'))
            d_logger.addHandler(d_handler)

    def ensure_appinfo(self):
        @wraps(self)
        async def wrapper(wrap, *args, **kwargs):
            await wrap._cache_app_info()
            # noinspection PyCallingNonCallable
            return await self(wrap, *args, **kwargs)

        return wrapper

    @ensure_appinfo
    async def generate_invite_link(self, *, permissions=discord.Permissions(70380544), guild=None):
        return discord.utils.oauth_url(self.cached_app_info.id, permissions=permissions, guild=guild)

    #######################################################################################################################

    def _gen_embed(self):
        """Provides a basic template for embeds"""
        e = discord.Embed()
        e.colour = 7506394
        e.set_footer(text='Helix ({})'.format(self.VERSION),
                     icon_url='https://imgur.com/a/wdNvSfZ')
        e.set_author(name=self.user.name, url='https://github.com/SinLess-Games/Helix',
                     icon_url=self.user.avatar_url)
        return e

    async def load(self, extension):
        self.load_extension(f'./Helix/cogs/{extension}')

    async def unload(self, extension):
        self.unload_extension(f'./Helix/cogs/{extension}')

    def run(self):
        print("Running bot...")
        try:
            self.loop.run_until_complete(self.start(self.TOKEN))

        except discord.errors.LoginFailure:
            # Add if token, else
            raise exceptions.HelpfulError(
                "Bot cannot login, bad credentials.",
                "Fix your token in the options file.  "
                "Remember that each field should be on their own line."
            )  # ^^^^ In theory self.config.auth should never have no items
        # super().run(self.TOKEN, reconnect=True)

    async def shutdown(self):
        print("Closing connection to Discord...")
        await super().close()

    async def close(self):
        print("Closing on keyboard interrupt...")
        await self.shutdown()

    async def on_connect(self):
        cT = datetime.now() + timedelta(
            hours=5, minutes=30
        )  # GMT+05:30 is Our TimeZone So.

        print(
            f"[ Log ] {self.user} Connected at {cT.hour}:{cT.minute}:{cT.second} / {cT.day}-{cT.month}-{cT.year}"
        )

    async def on_ready(self):
        d_logger = logging.getLogger('discord')
        for h in d_logger.handlers:
            if getattr(h, 'terminator', None) == '':
                d_logger.removeHandler(h)
                print()

        log.debug("Connection established, ready to go.")

        if self.init_ok:
            log.debug("Received additional READY event, may have failed to resume")
            return

        self.init_ok = True

        ################################

        log.info("Connected: {0}/{1}#{2}".format(
            self.user.id,
            self.user.name,
            self.user.discriminator
        ))

        # t-t-th-th-that's all folks!
        cT = datetime.now() + timedelta(
            hours=-7, minutes=00
        )  # GMT-07:00 is Our TimeZone So.

        print(
            f"[ Log ] {self.user} Ready at {cT.hour}:{cT.minute}:{cT.second} / {cT.day}-{cT.month}-{cT.year}"
        )
        print(f"[ Log ] GateWay WebSocket Latency: {self.latency * 1000:.1f} ms")
        self.config.client_id = (await self.application_info()).id
        print(f'[ Log ] Bot is ready! DEUS VULT!')

        config_activity = self.config.bot_activity
        activity = discord.Game(name=self.config.bot_status_text)

        await self.change_presence(status=config_activity, activity=activity)

        # Builds databases and tables, do not move from here, This works here and not in cogs.
        # TODO: find out if I can make it work in a cog, and if so how to.
        async for guild in self.fetch_guilds():
            Engine = create_engine(
                f'mysql+pymysql://{self.sql_user}:{self.sql_passwd}@{self.sql_host}/{guild.id}',
                echo=False)
            if not database_exists(Engine.url):
                create_database(Engine.url)
            else:
                # If DB exists prints database_exists
                print(database_exists(Engine.url))

            # usr = Users()
            # sts = Stats()
            # cfg = ServConfig()
            # bl = BlackList()
            # mut = Mutes()

            ServerList.__table__.create(bind=self.sql_engine, checkfirst=True)

            Users.__table__.create(bind=Engine, checkfirst=True)
            Bans.__table__.create(bind=Engine, checkfirst=True)
            Stats.__table__.create(bind=Engine, checkfirst=True)
            ServConfig.__table__.create(bind=Engine, checkfirst=True)
            BlackList.__table__.create(bind=Engine, checkfirst=True)
            Mutes.__table__.create(bind=Engine, checkfirst=True)
            Bots.__table__.create(bind=Engine, checkfirst=True)


bot = Helix()
