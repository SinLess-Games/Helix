import os
import logging
from datetime import datetime

#
# Setup of logging
#

# path for databases or config files
if not os.path.exists('Logs/'):
    os.mkdir('Logs/')

# set logging format
formatter = logging.Formatter("[{asctime}] [{levelname}] [{name}] {message}", style="{")

# create log file
date = datetime.today().strftime('%m-%d-%Y')

# logger for writing to file
log_access = f'Logs/{date}_events.log'
file_logger = logging.FileHandler(log_access)
file_logger.setLevel(logging.INFO)  # everything into the logging file
file_logger.setFormatter(formatter)

# logger for console prints
console_logger = logging.StreamHandler()
console_logger.setLevel(logging.WARNING)  # only important stuff to the terminal
console_logger.setFormatter(formatter)

# get new logger
logger = logging.getLogger('Helix-AI')
logger.setLevel(logging.INFO)

# register loggers
logger.addHandler(file_logger)
logger.addHandler(console_logger)
