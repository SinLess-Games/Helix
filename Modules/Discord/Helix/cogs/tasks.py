from datetime import datetime

import discord
from discord.ext import commands
from discord.ext import tasks
from sqlalchemy import *
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database

from Helix.utils.config import Config, ConfigDefaults
from Helix.utils.db_tools import ServerList, Users, Stats, Bans, Bots, ServConfig, BlackList, Mutes


class Task_Loop(commands.Cog):
    """
    Tasks for backend of bot, No commands for Users.
    """

    def __init__(self, client, config_file=None):
        if config_file is None:
            config_file = ConfigDefaults.Config_file

        self.config = Config(config_file)
        self.client = client
        self.index = 0
        self.update_24.start()

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

        # SqlAlchemy engine construction
        self.sql_engine = create_engine(
            f'mysql+pymysql://{self.sql_user}:{self.sql_passwd}@{self.sql_host}/{self.sql_ddb}', echo=False)
        if not database_exists(self.sql_engine.url):
            create_database(self.sql_engine.url)
        else:
            # If DB exists prints database_exists
            print(database_exists(self.sql_engine.url))

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """
            This event is called when a guild (server) is either created by the bot
             or when the bot joins a guild.
            Args:
                guild:
                    The Guild object of the joined guild.
            """
        Engine = create_engine(
            f'mysql+pymysql://{self.sql_user}:{self.sql_passwd}@{self.sql_host}/{guild.id}',
            echo=False)
        if not database_exists(Engine.url):
            create_database(Engine.url)
            Users.__table__.create(bind=Engine, checkfirst=True)
            Bans.__table__.create(bind=Engine, checkfirst=True)
            Stats.__table__.create(bind=Engine, checkfirst=True)
            ServConfig.__table__.create(bind=Engine, checkfirst=True)
            BlackList.__table__.create(bind=Engine, checkfirst=True)
            Mutes.__table__.create(bind=Engine, checkfirst=True)
            Bots.__table__.create(bind=Engine, checkfirst=True)
        else:
            # If DB exists prints database_exists
            # print(database_exists(Engine.url))
            pass
        Engine = create_engine(f'mysql+pymysql://{self.sql_user}:{self.sql_passwd}@{self.sql_host}/{self.sql_ddb}',
                               echo=False)

        channels = await guild.fetch_channels()
        members = await guild.fetch_members().flatten()
        channel_count = len(channels)
        members_count = len(members)
        server = guild.name

        with Session(Engine) as session:
            serv = ServerList()
            Guild_Exists = session.query(ServerList).filter_by(ServerID=guild.id).first()
            if not Guild_Exists:
                serv.ServerID = guild.id
                serv.ServerName = server.encode(encoding='UTF-8')
                serv.MemberCount = members_count
                serv.ChannelCount = channel_count
                serv.LastUpdate = datetime.now()
                session.add(serv)
                session.commit()
                session.close()

            else:
                session.query(ServerList).filter_by(ServerID=guild.id).update({
                    "ServerName": guild.name.encode(encoding='UTF-8'),
                    "bot_active": True,
                    "MemberCount": members,
                    "ChannelCount": channels,
                    "LastUpdate": datetime.now()
                }, synchronize_session="fetch")
                session.commit()
                session.close()

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        """
        This event is called when the bot is no longer in a guild (server).
        This can be either be:
         * The bot got kicked.
         * The bot got banned.
         * The bot left the guild.
         * The guild got deleted.
        Args:
            guild:
                The Guild object that's left by the bot.
        """
        Engine = create_engine(f'mysql+pymysql://{self.sql_user}:{self.sql_passwd}@{self.sql_host}/{self.sql_ddb}',
                               echo=False)

        with Session(Engine) as session:
            serv = ServerList()
            Guild_Exists = session.query(ServerList).filter_by(ServerID=guild.id).first()
            if Guild_Exists:
                serv.bot_active = False
                serv.LastUpdate = datetime.now()
                session.add(serv)
                session.commit()
                session.close()

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        """
            This event is called the guild (server) got updated.
            This can be either be:
             * Name changes.
             * AFK channel changes.
             * AFK timeout.
             * etc.
            Args:
                before:
                    The Guild object prior to the update.
                after:
                    The Guild object after the update.
            """
        Engine = create_engine(f'mysql+pymysql://{self.sql_user}:{self.sql_passwd}@{self.sql_host}/{self.sql_ddb}',
                               echo=False)

        channels = await after.fetch_channels()
        members = await after.fetch_members().flatten()
        server = after.name

        with Session(Engine) as session:
            serv = ServerList()
            Guild_Exists = session.query(ServerList).filter_by(ServerID=before.id).first()
            if not Guild_Exists:
                serv.ServerName = server.encode(encoding='UTF-8')
                serv.MemberCount = members
                serv.ChannelCount = channels
                serv.LastUpdate = datetime.now()
                session.add(serv)
                session.commit()
                session.close()

            else:
                session.query(ServerList).filter_by(ServerID=before.id).update({
                    "ServerName": after.name.encode(encoding='UTF-8'),
                    "bot_active": True,
                    "MemberCount": members,
                    "ChannelCount": channels,
                    "LastUpdate": datetime.now()
                }, synchronize_session="fetch")
                session.commit()
                session.close()

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        """
        This event is called when a new role is created in a guild (server).
        Args:
            role:
                The Role object of the created role.
        """
        # TODO: build sql for guild remove
        # COMING SOON
        pass

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        """
        This event is called when a new role is deleted in a guild (server).
        Args:
            role:
                The Role object of the deleted role.
        """
        # TODO: build sql for guild remove
        # COMING SOON
        pass

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        """
        This event is called when a role is updated in a guild (server).
        Args:
            before:
                The Role object of the original role.
            after:
                The Role object of the updated role.
        """
        # TODO: build sql for guild remove
        # COMING SOON
        pass

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        """
            This event is called when a member is banned from a guild (server).
            Args:
                guild:
                    The Guild object of where the user got banned from.
                user:
                    The User object of the one who got banned.
            """
        identity = guild.id
        Eng = create_engine(f'mysql+pymysql://{self.sql_user}:{self.sql_passwd}@{self.sql_host}/{identity}', echo=False)
        dt = datetime.today()
        date = dt
        with Session(Eng) as session:
            stats = Stats()
            bans = Bans()

            _stats = session.query(Stats).filter_by(Date=date).first()
            _Bans = session.query(Bans).filter_by(UserID=user.id).first()

            if not _Bans:
                bans.UserID = user.id
                bans.UserName = user.name
                bans.ban_date = date

                session.add(bans)
                session.commit()
                session.close()

            if not _stats:
                stats.MemberCount = 0
                stats.BanCount = 1
                stats.MessageDeletions = 0
                stats.MessageEdits = 0
                stats.RolesCount = 0
                stats.RoleChanges = 0
                stats.NameUpdates = 0
                stats.AvatarChanges = 0
                stats.IgnoredChannels = 0
                stats.Date = date

                session.add(stats)
                session.commit()
                session.close()

            else:
                data = session.query(Stats).filter_by(Date=date).first()
                session.query(Stats).filter_by(Date=date).update({
                    "Bancount": data.Bancount + 1
                }, synchronize_session="fetch")
                session.commit()
                session.close()

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        """
            This event is called when a member is unbanned from a guild (server).
            Args:
                guild:
                    The Guild object of where the user got unbanned from.
                user:
                    The User object of the one who got unbanned.
            """
        identity = guild.id
        Eng = create_engine(f'mysql+pymysql://{self.sql_user}:{self.sql_passwd}@{self.sql_host}/{identity}', echo=False)
        dt = datetime.today()
        date = dt
        with Session(Eng) as session:
            stats = Stats()

            _stats = session.query(Stats).filter_by(Date=date).first()
            _Bans = session.query(Bans).filter_by(UserID=user.id).first()

            if not _Bans:
                pass
            else:
                session.query(Bans).filter_by(UserID=user.id).delete()

            if not _stats:
                stats.MemberCount = 0
                stats.BanCount = 0
                stats.MessageDeletions = 0
                stats.MessageEdits = 0
                stats.RolesCount = 0
                stats.RoleChanges = 0
                stats.NameUpdates = 0
                stats.AvatarChanges = 0
                stats.IgnoredChannels = 0
                stats.Date = date

                session.add(stats)
                session.commit()
                session.close()

            else:
                data = session.query(Stats).filter_by(Date=date).first()
                session.query(Stats).filter_by(Date=date).update({
                    "Bancount": data.Bancount - 1
                }, synchronize_session="fetch")
                session.commit()
                session.close()

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        # print("message deletion detected")
        identity = message.guild.id
        Eng = create_engine(f'mysql+pymysql://{self.sql_user}:{self.sql_passwd}@{self.sql_host}/{identity}', echo=False)
        dt = datetime.today()
        date = dt.strftime('%Y-%m-%d')
        # print(f'The date var: {date}')
        with Session(Eng) as session:
            stats = Stats()
            stat = session.query(Stats).filter_by(Date=date).first()
            stat_date = stat.Date
            # print(f'The stats dat var: {stat_date}')

            _stats = session.query(Stats).filter_by(Date=date).first()

            if not _stats and date != stat_date:
                # print('No current date detected in stats table')
                stats.MemberCount = 0
                stats.BanCount = 0
                stats.MessageDeletions = 1
                stats.MessageEdits = 0
                stats.RolesCount = 0
                stats.RoleChanges = 0
                stats.NameUpdates = 0
                stats.AvatarChanges = 0
                stats.IgnoredChannels = 0
                stats.Date = date

                session.add(stats)
                session.commit()
                session.close()

            if str(date) == str(stat_date):
                # print('entry exists. Updating entry')
                data = session.query(Stats).filter_by(Date=date).first()
                session.query(Stats).filter_by(Date=date).update({
                    "MessageDeletions": data.MessageDeletions + 1
                }, synchronize_session="fetch")
                session.commit()
                session.close()

            else:
                pass

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        identity = before.guild.id
        Eng = create_engine(f'mysql+pymysql://{self.sql_user}:{self.sql_passwd}@{self.sql_host}/{identity}', echo=False)
        dt = datetime.today()
        date = dt.strftime('%Y-%m-%d')
        # print(f'The date var: {date}')
        with Session(Eng) as session:
            stats = Stats()
            stat = session.query(Stats).filter_by(Date=date).first()
            stat_date = stat.Date
            # print(f'The stats dat var: {stat_date}')

            _stats = session.query(Stats).filter_by(Date=date).first()

            if not _stats and date != stat_date:
                # print('No current date detected in stats table')
                stats.MemberCount = 0
                stats.BanCount = 0
                stats.MessageDeletions = 0
                stats.MessageEdits = 1
                stats.RolesCount = 0
                stats.RoleChanges = 0
                stats.NameUpdates = 0
                stats.AvatarChanges = 0
                stats.IgnoredChannels = 0
                stats.Date = date

                session.add(stats)
                session.commit()
                session.close()

            if str(date) == str(stat_date):
                # print('entry exists. Updating entry')
                data = session.query(Stats).filter_by(Date=date).first()
                session.query(Stats).filter_by(Date=date).update({
                    "MessageEdits": data.MessageEdits + 1
                }, synchronize_session="fetch")
                session.commit()
                session.close()

            else:
                pass

    @tasks.loop(hours=24)
    # Runs every 24 hours to update tables
    async def update_24(self):
        print("Updating...")
        async for guild in self.client.fetch_guilds():
            guild = await self.client.fetch_guild(guild.id)
            guild_roles = []
            for role in guild.roles:
                guild_roles.append(role)
            # print(f"guild roles: {str(guild_roles)}")

            Eng = create_engine(f'mysql+pymysql://{self.sql_user}:{self.sql_passwd}@{self.sql_host}/{guild.id}',
                                echo=False)
            Engine = create_engine(f'mysql+pymysql://{self.sql_user}:{self.sql_passwd}@{self.sql_host}/{self.sql_ddb}',
                                   echo=False)

            channels = await guild.fetch_channels()
            members = await guild.fetch_members().flatten()
            channel_count = len(channels)
            members_count = len(members)
            # add data to stats table
            bans = await guild.bans()
            ban_count = len(bans)
            dt = datetime.today()
            date = dt

            with Session(Engine) as session:
                serv = ServerList()
                GuildExists = session.query(ServerList).filter_by(ServerID=guild.id).first()
                if not GuildExists:
                    serv.ServerID = guild.id
                    serv.ServerName = guild.name.encode(encoding='UTF-8')
                    serv.MemberCount = members_count
                    serv.ChannelCount = channel_count
                    serv.LastUpdate = date
                    session.add(serv)
                    session.commit()
                    session.close()

                else:
                    session.query(ServerList).filter_by(ServerID=guild.id).update({
                        "ServerName": guild.name,
                        "MemberCount": members_count,
                        "ChannelCount": channel_count,
                        "LastUpdate": date
                    }, synchronize_session="fetch")
                    session.commit()
                    session.close()

            with Session(Eng) as session:
                stats = Stats()
                date = datetime.today()
                _stats = session.query(Stats).filter_by(Date=date).first()

                if not _stats:
                    stats.MemberCount = 0
                    stats.BanCount = ban_count
                    stats.MessageDeletions = 0
                    stats.MessageEdits = 0
                    stats.RolesCount = 0
                    stats.RoleChanges = 0
                    stats.NameUpdates = 0
                    stats.AvatarChanges = 0
                    stats.IgnoredChannels = 0
                    stats.Date = date

                    session.add(stats)
                    session.commit()
                    session.close()

                else:
                    data = session.query(Stats).filter_by(Date=date).first()
                    session.query(Stats).filter_by(Date=date).update({
                        "MessageEdits": data.MessageEdits + 0
                    }, synchronize_session="fetch")
                    session.commit()
                    session.close()

            Member: discord.Member
            async for Member in guild.fetch_members():
                member = await guild.fetch_member(Member.id)  # Fetches member object
                member_id = member.id  # Integer
                displayName = member.display_name  # String
                discriminator = member.discriminator  # String
                mention = member.mention  # String
                server = guild.name  # String
                _roles = []
                for role in member.roles:  # Iterates through each roll and adds them to a list
                    _roles.append(role.name)
                roles = str(_roles)
                # print(f"Guild: {guild.name}, User: {member.name}, roles: {_roles}, {roles}")

                dm = "coming soon"

                dt = datetime.today()
                date = dt
                engine1 = create_engine(f'mysql+pymysql://{self.sql_user}:{self.sql_passwd}@{self.sql_host}/{guild.id}',
                                        echo=False)
                with Session(engine1) as session:
                    usr = Users()
                    bot = Bots()

                    UserExists = session.query(Users).filter_by(UserID=member.id).first()
                    if not UserExists and not member.bot:
                        usr.UserID = member_id
                        usr.DisplayName = displayName.encode(encoding='UTF-8')
                        usr.Discriminator = discriminator.encode(encoding='UTF-8')
                        usr.Mention = mention.encode(encoding='UTF-8')
                        usr.DMChannel = dm.encode(encoding='UTF-8')
                        usr.Roles = roles.encode(encoding='UTF-8')
                        usr.Server = server.encode(encoding='UTF-8')
                        usr.PostCount = 0
                        usr.LastUpdate = date
                        session.add(usr)
                        session.commit()
                        session.close()

                    else:
                        session.query(Users).filter_by(UserID=member.id).update({
                            "DisplayName": displayName.encode(encoding='UTF-8'),
                            "Discriminator": discriminator.encode(encoding='UTF-8'),
                            "Mention": mention.encode(encoding='UTF-8'),
                            "DMChannel": dm.encode(encoding='UTF-8'),
                            "Roles": roles.encode(encoding='UTF-8'),
                            "LastUpdate": date
                        }, synchronize_session="fetch")
                        session.commit()
                        session.close()
                    if not UserExists and member.bot:
                        bot.UserID = member_id
                        bot.DisplayName = displayName.encode(encoding='UTF-8')
                        bot.Discriminator = discriminator.encode(encoding='UTF-8')
                        bot.Mention = mention.encode(encoding='UTF-8')
                        bot.DMChannel = dm.encode(encoding='UTF-8')
                        bot.Roles = roles.encode(encoding='UTF-8')
                        bot.Server = server.encode(encoding='UTF-8')
                        bot.usage = 0
                        bot.LastUpdate = date
                        session.add(bot)
                        session.commit()
                        session.close()
                    else:
                        session.query(Bots).filter_by(UserID=member.id).update({
                            "DisplayName": displayName.encode(encoding='UTF-8'),
                            "Discriminator": discriminator.encode(encoding='UTF-8'),
                            "Mention": mention.encode(encoding='UTF-8'),
                            "DMChannel": dm.encode(encoding='UTF-8'),
                            "Roles": roles.encode(encoding='UTF-8'),
                            "LastUpdate": date
                        }, synchronize_session="fetch")
                        session.commit()
                        session.close()

                # print(f"Adding users to: {guild.name} database; DBid: {guild.id}")


def setup(client):
    client.add_cog(Task_Loop(client))
