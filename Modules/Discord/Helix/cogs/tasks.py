import discord
import mysql.connector
import yaml
import logging

from discord.ext import commands
from discord.ext import tasks
from datetime import datetime
from utils.db_tools import connect, execute, execute_data_input, close, commit, execute_multi
from mysql.connector import errorcode


# Open Config file for TOKEN
with open("Configs/config.yml", 'r') as i:
    config = yaml.safe_load(i)

VERSION = config['Version']
logging.info(f"HeliX discord version: " + VERSION)
OWNER_NAME = config['OWNER_NAME']
OWNER_ID = config['bot_owner_id']
PREFIX = config['Prefix']


class tasks(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.index = 0
        self.update.start()

    @tasks.loop(hours=24)
    # Runs every 24 hours to update tables
    async def update(self):
        print("Updating...")
        async for guild in self.client.fetch_guilds():
            channels = await guild.fetch_channels()
            members = await guild.fetch_members().flatten()
            channel_count = len(channels)
            members_count = len(members)
            update_date = datetime.now()
            # add data to stats table
            bans = await guild.bans()
            ban_count = len(bans)
            add_bans = (f"INSERT INTO stats member_count='{members_count}, bans='{ban_count})"
                        )
            connect(guild.id)
            execute(
                f'''
                    INSERT INTO logging server='{str(guild.id)}', message_edit='{0}', message_deletion='{0}', role_changes='{0}', name_update='{0}', member_movement='{0}', avatar_changes='{0}', bans='{0}', ignored_channels='{None}'
                '''
            )
            execute(add_bans)
            close()
            async for member in guild.fetch_members():
                member_id = member.id
                displayName = member.display_name
                discriminator = member.discriminator
                mention = member.mention
                # update existing
                User = discord.Member
                dm = User.dm_channel
                update_user = (
                    f"UPDATE users SET display_name='{displayName}', discriminator='{discriminator}', mention='{mention}', dm_channel='{dm}', server='{guild.name}', id='{member.id}', names='{str(displayName)}' WHERE user_id='{member_id}'")
                update_Guild = (
                    "INSERT INTO servers Values prefix='{}', id='{}', Member_Count='{}', Channels='{}', Last_Update='{}' WHERE Server_ID='{}'".format(
                        PREFIX, guild.id, members_count, channel_count, update_date, guild.id))
                connect(f"{guild.id}")
                print("Adding users to: " + f"{guild.id}")
                execute(update_user)
                close()
                connect("discord")
                execute(update_Guild)
                close()

    @tasks.loop(minutes=5)
    async def update(self):
        print("\033[0;32m Adding data tables to DBs")
        async for guild in self.client.fetch_guilds():
            table = (
                "CREATE TABLE IF NOT EXISTS users (rID BIGINT(10) NOT NULL PRIMARY KEY AUTO_INCREMENT, user_id BIGINT(30) UNIQUE, display_name BLOB NULL, discriminator VARCHAR(5), mention VARCHAR(50), dm_channel VARCHAR(50), roles text, server text, location text, id text, names text, postcount int, retard int, sicklad int);"
            )
            connect(guild.id)
            execute(table)
            table = (
                "CREATE TABLE IF NOT EXISTS blacklist (ID BIGINT(10) NOT NULL PRIMARY KEY AUTO_INCREMENT, word VARCHAR(50) UNIQUE, Last_Update DATETIME);"
            )
            execute(table)
            table = (
                "CREATE TABLE IF NOT EXISTS stats (days BIGINT(10) NOT NULL PRIMARY KEY AUTO_INCREMENT, member_count BIGINT(20), bans BIGINT(20));"
            )
            execute(table)
            table = (
                "CREATE TABLE IF NOT EXISTS mutes (UserID BIGINT(10), RoleIDs text, EndTime text);"
            )
            execute(table)
            table = (
                "CREATE TABLE IF NOT EXISTS logging (server text, message_edit boolean, message_deletion boolean,role_changes boolean, name_update boolean, member_movement boolean,avatar_changes boolean, bans boolean, ignored_channels text);"
            )
            execute(table)
            table = (
                "CREATE TABLE IF NOT EXISTS greetings (guild_id text, greet_channel text, greet_message text, farewell_message text, ban_message text);"
            )
            execute(table)
            close()
            table1 = (
                "CREATE TABLE IF NOT EXISTS messages (unix real, timestamp timestamp, content text, id text, author text, channel text, server text);"
            )
            connect(guild.id)
            execute(table1)
            table1 = (
                "CREATE TABLE IF NOT EXISTS config (guild_id text, ignored_channels text, commands text, enabled boolean);"
            )
            execute(table1)
            table1 = (
                "CREATE TABLE IF NOT EXISTS userconfig (guild_id text, user_id text, command text, status boolean, plonked boolean);"
            )
            execute(table1)
            table1 = (
                "CREATE TABLE IF NOT EXISTS channelconfig (guild_id text, channel_id text, commands text, ignored_channels text);"
            )
            execute(table1)
            table1 = (
                "CREATE TABLE IF NOT EXISTS role_config (whitelisted text, unique_roles boolean, guild_id text, autoroles text);"
            )
            execute(table1)
            close()
            connect(guild.id)
            execute("CREATE TABLE IF NOT EXISTS role_alias (guild_id text(50), role_id text(50), role_name text(50), alias text(50));")
            close()


def setup(client):
    client.add_cog(tasks(client))
