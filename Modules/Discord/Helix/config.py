import logging

import yaml

log = logging.getLogger(__name__)


class Config:
    # noinspection PyUnresolvedReferences
    def __init__(self, config_file):
        try:
            with open("Configs/config.yml", "w+", encoding="utf-8") as file:
                self.config = yaml.safe_load(file)

        except:
            yaml.safe_dump(data, encoding="utf-8", )
