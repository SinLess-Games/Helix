import sentry_sdk
import discord
import yaml
from flask import Flask
from appmap.flask import AppmapFlask
from Helix import bot

app = Flask(__name__)

appmap_flask = AppmapFlask(app)

sentry_sdk.init(
    "https://fe349234191e4e86a83c8cd381068ab4@o901570.ingest.sentry.io/5994911",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)

with open("Configs/config.yml", "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)

TOKEN = config['Token']
VERSION = config['Version']


if __name__ == "__main__":
    bot.run(TOKEN)
