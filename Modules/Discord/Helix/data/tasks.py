import logging
from datetime import datetime

import discord
import yaml
from discord.ext import commands
from discord.ext import tasks
from sqlalchemy import *
from sqlalchemy.orm import Session

from Helix.utils.db_tools import Stats, Users, ServerList

# Open Config file for TOKEN
with open("Helix/Configs/config.yml", 'r') as i:
    config = yaml.safe_load(i)

VERSION = config['Version']
logging.info(f"HeliX discord version: " + str(VERSION))
OWNER_NAME = config['Owner_Name']
OWNER_ID = config['bot_owner_id']

with open("Helix/Configs/config.yml", 'r') as i:
    cfg = yaml.safe_load(i)

# !SET THOSE VARIABLES TO MAKE THE COG FUNCTIONAL!
version = cfg['Version']
host = cfg['SQL_Host']
user = cfg['SQL_UserName']
passwd = cfg['SQL_Password']
db = cfg['DefaultDatabase']


class tasks(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.index = 0
        self.update.start()

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
        engine = create_engine(f'mysql+pymysql://{user}:{passwd}@{host}/{id}', echo=False)
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
            Engine = create_engine(f'mysql+pymysql://{user}:{passwd}@{host}/{db}', echo=False)
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

                serv.ServerID = guild.id
                serv.ServerName = guild.name
                serv.MemberCount = members_count
                serv.ChannelCount = channel_count
                serv.LastUpdate = date

                session.add(serv)
                session.commit()
                session.close()

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        id = message.guild.id
        engine = create_engine(f'mysql+pymysql://{user}:{passwd}@{host}/{id}', echo=False)
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
        engine = create_engine(f'mysql+pymysql://{user}:{passwd}@{host}/{id}', echo=False)
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
    async def update(self):
        print("Updating...")
        async for guild in self.client.fetch_guilds():
            engine = create_engine(f'mysql+pymysql://{user}:{passwd}@{host}/{guild.id}', echo=False)
            Engine = create_engine(f'mysql+pymysql://{user}:{passwd}@{host}/{db}', echo=False)
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
                member_id = member.id
                displayName = member.display_name
                discriminator = member.discriminator
                mention = member.mention
                roles = str(member.roles)
                # update existing
                User = discord.Member
                dm = User.dm_channel
                dt = datetime.today()
                date = dt
                engine = create_engine(f'mysql+pymysql://{user}:{passwd}@{host}/{guild.id}', echo=False)
                with Session(engine) as session:
                    usr = Users()

                    UserExists = session.query(Users).filter_by(UserID=member.id).first()
                    if not UserExists:
                        usr.UserID = member_id
                        usr.DisplayName = displayName
                        usr.Discriminator = discriminator
                        usr.Mention = mention
                        usr.DMChannel = dm
                        usr.Roles = roles
                        usr.Server = guild.name
                        usr.LastUpdate = date
                        session.add(usr)
                        session.commit()
                        session.close()

                    else:
                        session.query(Users).filter_by(UserID=member.id).update({
                            "DisplayName": displayName,
                            "Discriminator": discriminator,
                            "Mention": mention,
                            "DMChannel": dm,
                            "Roles": roles,
                            "PostCount": 0,
                            "LastUpdate": date
                        }, synchronize_session="fetch")
                        session.commit()
                        session.close()

                print("Adding users to: " + f"{guild.id}")


def setup(client):
    client.add_cog(tasks(client))
