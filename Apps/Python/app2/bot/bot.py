# Name Helix

import datetime
import traceback
import logging
import sys
import os
from datetime import datetime
import discord
import yaml
from log_setup import logger
from discord.ext import commands
from util.db_tools import connect, execute, execute_data_input, close
import mysql.connector
from mysql.connector import errorcode

# Discord Intents

intents = discord.Intents.default()
intents.typing = True
intents.presences = True
intents.members = True
intents.messages = True
guild_subscriptions = True
fetch_offline_members = True

client = commands.Bot(command_prefix='H!', intents=intents)
# client.remove_command('help')

# Open Config file for TOKEN
with open("config.yml", 'r') as i:
    cfg = yaml.safe_load(i)

TOKEN = cfg['Helix_BOT']['Token']
VERSION = cfg['Helix_BOT']['Version']
OWNER_NAME = cfg['Helix_BOT']['OWNER_NAME']
OWNER_ID = cfg['Helix_BOT']['OWNER_ID']
PREFIX = cfg['Helix_BOT']['PREFIX']

discord_logger = logging.getLogger('discord')
discord_logger.setLevel(logging.CRITICAL)
log = logging.getLogger()
log.setLevel(logging.INFO)
handler = logging.FileHandler(filename="Helix.log", encoding='utf-8', mode='w')
log.addHandler(handler)
log = logging.getLogger(__name__)


async def on_command_error(self, ctx, error):
    if isinstance(error, commands.NoPrivateMessage):
        await ctx.author.send('This command cannot be used in private messages.')
    elif isinstance(error, commands.DisabledCommand):
        await ctx.author.send('Sorry. This command is disabled and cannot be used.')
    elif isinstance(error, commands.CommandInvokeError):
        print(f'In {ctx.command.qualified_name}:', file=sys.stderr)
        traceback.print_tb(error.original.__traceback__)
        print(
            f'{error.original.__class__.__name__}: {error.original}', file=sys.stderr)


@client.event
async def on_ready():
    """!
        function called when the bot is ready. emits the '[Bot] has connected' message
        """
    """A lot of commands are dependant on information found in the database
    This abuses the api into giving me the required information
    useful for when the bot joins a server while offline"""

    logger.info(f"Bot has connected, active on {len(client.guilds)} guilds")

    print('Logged in as:')
    print('Username: ' + client.user.name)
    print('ID: ' + str(client.user.id))
    print('------')

    for guild in client.guilds:
        # create server table if it does not exist
        database = 'discord'
        connect(database)
        create_server_table = (
            "CREATE TABLE IF NOT EXISTS servers (rID BIGINT(10) NOT NULL PRIMARY KEY AUTO_INCREMENT UNIQUE, id text, log_channel text, twitch_channel text, welcome_message text, bot_channel text, prefix text, Server_Name VARCHAR(50), Server_ID BIGINT(30) UNIQUE, Member_Count BIGINT(20), Channels BIGINT(20), Last_Update DATETIME)"
        )
        execute(create_server_table)
        close()

        # Add server info into database discord table servers
        channels = await guild.fetch_channels()
        members = await guild.fetch_members().flatten()
        channel_count = len(channels)
        members_count = len(members)
        update_date = datetime.now()
        add_Guild = ("INSERT INTO servers"
                     "(Server_Name, Server_ID, Member_Count, Channels, Last_Update)"
                     "VALUES (%s, %s, %s, %s, %s)"
                     )
        data_guild = (guild.name, guild.id, members_count, channel_count, update_date)
        connect('discord')
        execute_data_input(add_Guild, data_guild)
        close()
        # create server specific databases
        connect('discord')
        data_base = ("CREATE DATABASE IF NOT EXISTS`{}`".format(guild.id))
        execute(data_base)
        close()

        try:
            database = guild.id
            connect(database)
            # create tables for specific databases
            table = (
                "CREATE TABLE IF NOT EXISTS users (rID BIGINT(10) NOT NULL PRIMARY KEY AUTO_INCREMENT, user_id BIGINT(30) UNIQUE, display_name BLOB NULL, discriminator VARCHAR(5), mention VARCHAR(50), dm_channel VARCHAR(50), roles text, server text, location text, id text, names text, postcount int, retard int, sicklad int);"
                "CREATE TABLE IF NOT EXISTS blacklist (ID BIGINT(10) NOT NULL PRIMARY KEY AUTO_INCREMENT, word VARCHAR(50) UNIQUE);"
                "CREATE TABLE IF NOT EXISTS stats (days BIGINT(10) NOT NULL PRIMARY KEY AUTO_INCREMENT, member_count BIGINT(20), bans BIGINT(20));"
                "CREATE TABLE IF NOT EXISTS mutes (UserID BIGINT(10), RoleIDs text, EndTime text);"
                "CREATE TABLE IF NOT EXISTS logging (server text, message_edit boolean, message_deletion boolean,role_changes boolean, name_update boolean, member_movement boolean,avatar_changes boolean, bans boolean, ignored_channels text);"
                "CREATE TABLE IF NOT EXISTS greetings (guild_id text, greet_channel text, greet_message text, farewell_message text, ban_message text);"
                "CREATE TABLE IF NOT EXISTS config (guild_id text, ignored_channels text, commands text, enabled boolean);"
                "CREATE TABLE IF NOT EXISTS userconfig (guild_id text, user_id text, command text, status boolean, plonked boolean);"
                "CREATE TABLE IF NOT EXISTS channelconfig (guild_id text, channel_id text, commands text, ignored_channels text);"
                "CREATE TABLE IF NOT EXISTS role_config (whitelisted text, unique_roles boolean, guild_id text, autoroles text);"
                "CREATE TABLE IF NOT EXISTS role_alias (guild_id text, role_id text, role_name text, alias text, UNIQUE (guild_id, alias));"
            )
            connect(guild.id)
            execute(table)
            close()
            table1 = (
                "CREATE TABLE IF NOT EXISTS messages (unix real, timestamp timestamp, content text, id text, author text, channel text, server text);"
            )
            connect(guild.id)
            execute(table1)
            close()

            # add data to stats table
            bans = await guild.bans()
            ban_count = len(bans)
            add_bans = ("INSERT INTO stats"
                        "(member_count, bans)"
                        "VALUES (%s, %s)"
                        )
            data_bans = (members_count, ban_count)
            connect(guild.id)
            execute_data_input(add_bans, data_bans)
            execute_data_input('''INSERT INTO logging
                                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                               (str(guild.id), 1, 1, 1, 1, 1, 1, 1, None))
            close()

            # Add users to user tables
            async for member in guild.fetch_members():
                member_id = member.id
                displayName = member.display_name
                discriminator = member.discriminator
                mention = member.mention
                add_user = ("INSERT INTO users"
                            "(user_id, display_name, discriminator, mention, names, id, server)"
                            "VALUES (%s, %s, %s, %s, %s, %s, %s)"
                            )
                user_data = (member_id, displayName, discriminator, mention, displayName, member_id, guild.name)
                connect(guild.id)
                execute_data_input(add_user, user_data)
                close()

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print(f'\033[1;31m Something is wrong with your user name or password')
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print(f'\033[1;31m Database does not exist')
            elif err.errno == errorcode.ER_DUP_ENTRY:
                print(f'\033[1;32m Entry already exists.')
                print("UPDATING..........")
                for guild in client.guilds:
                    channels = await guild.fetch_channels()
                    members = await guild.fetch_members().flatten()
                    channel_count = len(channels)
                    members_count = len(members)
                    update_date = datetime.now()
                    bans = await guild.bans()
                    ban_count = len(bans)
                    async for member in guild.fetch_members():
                        member_id = member.id
                        displayName = member.display_name
                        discriminator = member.discriminator
                        mention = member.mention
                        print(f'\033[5;32m UPDATING......')
                        # update existing
                        User = discord.Member
                        dm = User.dm_channel
                        update_user = (
                            "UPDATE users SET display_name='{}', discriminator='{}', mention='{}', dm_channel='{}', server='{}', id='{}', names='{}' WHERE user_id='{}'".format(
                                displayName, discriminator, mention, dm, guild.name, member.id, str(displayName),
                                member_id))
                        update_Guild = (
                            "UPDATE servers SET prefix='{}', id='{}', Member_Count='{}', Channels='{}', Last_Update='{}' WHERE Server_ID='{}'".format(
                                PREFIX, guild.id, members_count, channel_count, update_date, guild.id))
                        connect(guild.id)
                        execute(update_user)
                        close()
                        connect("discord")
                        execute(update_Guild)
                        close()
            else:
                print(f'\033[1;31m {err}')


@client.command()
async def message(ctx, user: discord.Member, *, message=None):
    message = "Welcome to the server!"
    embed = discord.Embed(title=message)
    await user.send(embed=embed)


@client.command()
async def load(self):
    client.load_extension(f'cogs.extension')


@client.command()
async def unload(self):
    client.unload_extension(f'cogs.extension')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


def run_bot():
    client.run(TOKEN)
