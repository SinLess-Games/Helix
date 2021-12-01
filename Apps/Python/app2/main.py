import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon
from utils import db_tools, email_sender
from bot.bot import run_bot
from utils.register import login, register


def window():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(1200, 300, 500, 500)
    win.setWindowTitle("HELIX")
    win.setWindowIcon(QIcon("logo2.png"))
    win.show()
    sys.exit(app.exec_())


def starting():
    starting_counter = 0

    window()
    starting_counter = 1
    run_bot()
    starting_counter = 2
