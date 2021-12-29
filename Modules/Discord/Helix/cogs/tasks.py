from datetime import datetime

import discord
from discord.ext import commands
from discord.ext import tasks
from sqlalchemy import *
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database

from Helix.utils.config import Config, ConfigDefaults
from Helix.utils.db_tools import ServerList, Users, Stats


class Task_Loop(commands.Cog):

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
    async def on_guild_update(self):
        # TODO: build sql for guild update
        pass

    @commands.Cog.listener()
    async def on_guild_remove(self):
        # TODO: build sql for guild remove
        pass

    @commands.Cog.listener()
    async def on_member_ban(self, guild):
        id = guild.id
        engine = create_engine(f'mysql+pymysql://{self.sql_user}:{self.sql_passwd}@{self.sql_host}/{id}', echo=False)
        dt = datetime.today()
        date = dt
        with Session(engine) as session:
            stats = Stats()

            _stats = session.query(Stats).filter_by(Date=date).first()

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
    async def on_member_unban(self):
        # TODO: build sql for member unban
        pass

    @commands.Cog.listener()
    async def on_guild_join(self):
        async for guild in self.client.fetch_guilds():
            Engine = create_engine(f'mysql+pymysql://{self.sql_user}:{self.sql_passwd}@{self.sql_host}/{self.sql_ddb}',
                                   echo=False)
            dt = datetime.today()
            date = dt

            channels = await guild.fetch_channels()
            members = await guild.fetch_members().flatten()
            server = guild.name
            channel_count = len(channels)
            members_count = len(members)
            # add data to stats table
            bans = await guild.bans()
            ban_count = len(bans)
            dt = datetime.today()
            date = dt

            with Session(Engine) as session:
                serv = ServerList()
                Guild_Exists = session.query(ServerList).filter_by(ServerID=guild.id).first()
                if not Guild_Exists:
                    serv.ServerID = guild.id
                    serv.ServerName = server.encode(encoding='UTF-8')
                    serv.MemberCount = members
                    serv.ChannelCount = channels
                    serv.LastUpdate = datetime.now()
                    session.add(serv)
                    session.commit()
                    session.close()

                else:
                    session.query(ServerList).filter_by(ServerID=guild.id).update({
                        "ServerName": guild.name,
                        "MemberCount": members,
                        "ChannelCount": channels,
                        "LastUpdate": datetime.now()
                    }, synchronize_session="fetch")
                    session.commit()
                    session.close()

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        id = message.guild.id
        engine = create_engine(f'mysql+pymysql://{self.sql_user}:{self.sql_passwd}@{self.sql_host}/{id}', echo=False)
        dt = datetime.today()
        date = dt
        with Session(engine) as session:
            stats = Stats()

            _stats = session.query(Stats).filter_by(Date=date).first()

            if not _stats:
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

            else:
                data = session.query(Stats).filter_by(Date=date).first()
                session.query(Stats).filter_by(Date=date).update({
                    "MessageDeletions": data.MessageDeletions + 1
                }, synchronize_session="fetch")
                session.commit()
                session.close()

    @commands.Cog.listener()
    async def on_message_edit(self, message):
        id = message.guild.id
        engine = create_engine(f'mysql+pymysql://{self.sql_user}:{self.sql_passwd}@{self.sql_host}/{id}', echo=False)
        dt = datetime.today()
        date = dt
        with Session(engine) as session:
            stats = Stats()

            _stats = session.query(Stats).filter_by(Date=date).first()

            if not _stats:
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

            else:
                data = session.query(Stats).filter_by(Date=date).first()
                session.query(Stats).filter_by(Date=date).update({
                    "MessageEdits": data.MessageEdits + 1
                }, synchronize_session="fetch")
                session.commit()
                session.close()

    @tasks.loop(hours=24)
    # Runs every 24 hours to update tables
    async def update_24(self):
        print("Updating...")
        async for guild in self.client.fetch_guilds():
            engine = create_engine(f'mysql+pymysql://{self.sql_user}:{self.sql_passwd}@{self.sql_host}/{guild.id}',
                                   echo=False)
            Engine = create_engine(f'mysql+pymysql://{self.sql_user}:{self.sql_passwd}@{self.sql_host}/{self.sql_ddb}',
                                   echo=False)
            dt = datetime.today()
            date = dt

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
                    serv.ServerName = guild.name
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

            with Session(engine) as session:
                stats = Stats()
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

            async for member in guild.fetch_members():
                member_id = member.id  # Integer
                displayName = member.display_name  # String
                discriminator = member.discriminator  # String
                mention = member.mention  # String
                roles = str(member.roles)  # List
                server = guild.name  # String
                # update existing
                User = discord.Member
                dm = str(User.dm_channel)
                dt = datetime.today()
                date = dt
                engine1 = create_engine(f'mysql+pymysql://{self.sql_user}:{self.sql_passwd}@{self.sql_host}/{guild.id}',
                                        echo=False)
                with Session(engine1) as session:
                    usr = Users()

                    UserExists = session.query(Users).filter_by(UserID=member.id).first()
                    if not UserExists:
                        usr.UserID = member_id
                        usr.DisplayName = displayName.encode(encoding='UTF-8')
                        usr.Discriminator = discriminator.encode(encoding='UTF-8')
                        usr.Mention = mention.encode(encoding='UTF-8')
                        usr.DMChannel = dm.encode(encoding='UTF-8')
                        usr.Roles = roles.encode(encoding='UTF-8')  # TODO: needs fixed, returns none type list
                        usr.Server = server.encode(encoding='UTF-8')
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
                            "PostCount": 0,
                            "LastUpdate": date
                        }, synchronize_session="fetch")
                        session.commit()
                        session.close()

                print(f"Adding users to: {guild.name} database; DBid: {guild.id}")


def setup(client):
    client.add_cog(Task_Loop(client))
