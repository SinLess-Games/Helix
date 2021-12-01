import mysql.connector
from mysql.connector import errorcode


def exists():
    File = open("data_bool.txt", "r")
    return File.read()


def write(ctx):
    File = open("data_bool.txt", "w")
    File.write(ctx)


def connect(database_name):
    global cnx
    global cursor
    user = "Admin"
    try:
        cnx = mysql.connector.connect(
            host='192.168.86.78',
            port='3306',
            user=user,
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
        # print(f'\033[1;32m Connected to MySQL Server version\033[0;33m ', db_Info)
        cursor = cnx.cursor()
        cursor.execute("select database();")
        record1 = cursor.fetchone()
        record = record1[0]
        # print(f'\033[1;32m You\'re connected to database: \033[3;34m', record)


def fetchall():
    cursor.fetchall()


def execute(ctx):
    try:
        write('False')
        # print(f'Query:\n' + str(ctx))
        cursor.execute(ctx)
        cnx.commit()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            # print(f'\033[1;31m Something is wrong with your user name or password')
            return
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            # print(f'\033[1;31m Database does not exist')
            return
        elif err.errno == errorcode.ER_DUP_ENTRY:
            # print(f'\033[1;32m Entry already exists.')
            write('True ')
            return
        else:
            print(f'\033[1;91m {err}\n' + f"{ctx}")


def execute_multi(ctx):
    try:
        write('False')
        cursor.execute(ctx, multi=True)
        cnx.commit()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            # print(f'\033[1;31m Something is wrong with your user name or password')
            return
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            # print(f'\033[1;31m Database does not exist')
            return
        elif err.errno == errorcode.ER_DUP_ENTRY:
            # print(f'\033[1;32m Entry already exists.')
            write('True ')
            return
        else:
            print(f'\033[1;91m {err}\n' + f"{ctx}")


def execute_data_input(ctx, ctx1):
    try:
        write('False')
        # print(f'Query:\n' + str(ctx) + '\n' + str(ctx1))
        cursor.execute(ctx, ctx1)
        cnx.commit()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            # print(f'\033[1;31m Something is wrong with your user name or password')
            return
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            # print(f'\033[1;31m Database does not exist')
            return
        elif err.errno == errorcode.ER_DUP_ENTRY:
            # print(f'\033[1;32m entry already exists.')
            write('True ')
            return
        else:
            print(f'\033[1;91m {err}\n' + f"{ctx} \n {ctx1}")


def close():
    cursor.close()
    cnx.close()
    # print(f"\033[0;32m cnxection Closed. \n")


def commit():
    cnx.commit()


def fetchone():
    cursor.fetchone()
