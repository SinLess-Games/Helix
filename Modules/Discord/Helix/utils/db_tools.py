import sqlalchemy
import yaml
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

# Opens the config and reads it, no need for changes unless you'd like to change the library (no need to do so unless
# having issues with ruamel)
with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)

_Version_ = sqlalchemy.__version__
Base = declarative_base()

metadata_obj = MetaData()


# ServerList table construction
# TODO: Go through code verify location where each column is used
class ServerList(Base):
    # Table name
    __tablename__ = "ServerList"

    # Columns (name = construction)
    rID = Column(Integer, primary_key=True, autoincrement=True)
    ServerID = Column(BigInteger)
    ServerName = Column(String(200))
    MemberCount = Column(Integer)
    ChannelCount = Column(Integer)
    Prefix = Column(String(200), default='H!')
    WelcomeEnabled = Column(BOOLEAN, default=False)
    LeaveEnabled = Column(BOOLEAN, default=False)
    AutoModEnabled = Column(BOOLEAN, default=True)
    MusicEnabled = Column(BOOLEAN, default=True)
    LastUpdate = Column(DATE)


# Users table construction
# TODO: Go through code verify location where each column is used
class Users(Base):  # tasks.py handles this table
    __tablename__ = "Users"

    rID = Column(BigInteger, primary_key=True, autoincrement=True)
    UserID = Column(BigInteger)
    DisplayName = Column(BLOB)
    Discriminator = Column(VARCHAR(50))
    Mention = Column(VARCHAR(50))
    DMChannel = Column(VARCHAR(50))
    Roles = Column(String(500))
    Server = Column(String(200))
    PostCount = Column(Integer)
    LastUpdate = Column(DATE)


# Stats table Construction
# TODO: Go through code verify location where each column is used
class Stats(Base):  # tasks.py handles this table
    __tablename__ = "Stats"

    ID = Column(Integer, primary_key=True, autoincrement=True)
    Days = Column(Integer, autoincrement=True)
    MemberCount = Column(Integer)
    BanCount = Column(Integer)
    MessageEdits = Column(Integer)
    MessageDeletions = Column(Integer)
    RolesCount = Column(Integer)
    RoleChanges = Column(Integer)
    NameUpdates = Column(Integer)
    AvatarChanges = Column(Integer)
    IgnoredChannels = Column(Integer)
    Date = Column(DATE)


# Config table Construction
# TODO: Go through code verify location where each column is used
class Config(Base):
    __tablename__ = "Config"

    ID = Column(BigInteger, primary_key=True, autoincrement=True)
    WhiteListed = Column(String(200))
    UniqueRoles = Column(String(200))
    AutoRoles = Column(String(200))
    IgnoredChannels = Column(String(200))
    Commands = Column(String(200))
    WelcomeChannelID = Column(Integer)
    LeaveMessage = Column(String(200))
    WelcomeMessage = Column(String(200))
    LastUpdate = Column(DATE)


# Blacklist table Construction (for auto Mod)
# TODO: Go through code verify location where each column is used
class BlackList(Base):  # mod.py handles this table
    __tablename__ = "BlackList"

    ID = Column(Integer, primary_key=True, autoincrement=True)
    Word = Column(String(200))
    AddDate = Column(DATE)


# Mute table Construction
# TODO: Go through code verify location where each column is used
class Mutes(Base):
    __tablename__ = "Mutes"

    ID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(Integer)
    UserName = Column(String(200))
    Roles = Column(String(200))
    EndTime = Column(DATETIME)
