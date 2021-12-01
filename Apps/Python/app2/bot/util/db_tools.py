import mysql.connector
from mysql.connector import errorcode
import sys


def exists():
    File = open("data_bool.txt", "r")
    return File.read()


def write(ctx):
    File = open("data_bool.txt", "w")
    File.write(ctx)


def connect(self):
    global cnx
    global cursor
    try:
        database_name = self
        cnx = mysql.connector.connect(
            host='192.168.86.41',
            user='admin',
            password='Shellshocker93!',
            database=f"{database_name}"
        )
    # exception occurred
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print(f'\033[1;31m Something is wrong with your user name or password')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print(f'\033[1;31m Database does not exist')
        else:
            print(f'\033[1;31m {err}')

    if cnx.is_connected():
        db_Info = cnx.get_server_info()
        print(f'\033[1;32m Connected to MySQL Server version\033[0;33m ', db_Info)
        cursor = cnx.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print(f'\033[1;32m You\'re connected to database: \033[3;34m', record)


def cursor():
    cnx.cursor()


def execute(ctx):
    try:
        write('False')
        cursor.execute(ctx)
        cnx.commit()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print(f'\033[1;31m Something is wrong with your user name or password')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print(f'\033[1;31m Database does not exist')
        elif err.errno == errorcode.ER_DUP_ENTRY:
            print(f'\033[1;32m Entry already exists.')
            write('True ')
        else:
            print(f'\033[1;31m {err}')


def execute_data_input(ctx, ctx1):
    try:
        write('False')
        cursor.execute(ctx, ctx1)
        cnx.commit()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print(f'\033[1;31m Something is wrong with your user name or password')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print(f'\033[1;31m Database does not exist')
        elif err.errno == errorcode.ER_DUP_ENTRY:
            print(f'\033[1;32m entry already exists.')
            write('True ')
        else:
            print(f'\033[1;31m {err}')


def close():
    cursor.close()
    cnx.close()
    print(f"\033[0;32m Connection Closed. \n")
