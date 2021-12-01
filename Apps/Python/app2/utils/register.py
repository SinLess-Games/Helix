from utils.db_tools import connect, execute, execute_data_input, close, fetch_all
import bcrypt
import re
import mysql.connector
from mysql.connector import errorcode

granted = False
option = input("Login or Register (Login,Reg): ")
global HASHED_PASSWORD
global name

global cnx
global cursor


def grant():
    global granted
    granted = True


def register(name, password):
    try:
        database_name = "Web_Permissions"
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

    name = input("Enter your name: ")

    try:
        query = f"SELECT LogIn_ID FROM Web_User WHERE LogIn_ID = '{name}'"
        cursor.execute(query)
        rows = cursor.fetchall()
        new = rows[0]
        name1 = new[0]
        if name1 == name:
            print('Username Taken')
    except IndexError:
        SpecialSym = ['$', '@', '#', '%', '!']
        loop3 = True
        while loop3:
            password = input("Enter a password: ")
            if len(password) < 8:
                print('length should be at least 8')
            if len(password) > 20:
                print('length should be not be greater than 20')
            elif not any(char.isdigit() for char in password):
                print('Password should have at least one numeral')
            if not any(char.isupper() for char in password):
                print('Password should have at least one uppercase letter')
            if not any(char.islower() for char in password):
                print('Password should have at least one lowercase letter')
            if not any(char in SpecialSym for char in password):
                print('Password should have at least one of the symbols $, @, #, %, !')
            else:
                print("Your password seems fine")
                loop3 = False
                register(name, password)
                break
    cnx.close()


def login():
    try:
        database_name = "Web_Permissions"
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

    uid = input("Enter your name: ")

    try:
        query = f"SELECT LogIn_ID FROM Web_User WHERE LogIn_ID = '{uid}'"
        cursor.execute(query)
        rows = cursor.fetchall()
        new = rows[0]
        name1 = new[0]
        if name1 == uid:
            loop1 = True
            while loop1:
                password = input("Enter your password: ")
                USER_DATA = f"SELECT Login_Password From Web_User Where LogIn_ID = '{uid}'"
                cursor.execute(USER_DATA)
                rows = cursor.fetchall()
                new = rows[0]
                pwdh = new[0]
                new = f"b'{pwdh}.'"

                if bcrypt.checkpw(password.encode('utf8'), pwdh.encode('utf8')):
                    print("Login Successful")
                    grant()
                    loop1 = False
                else:
                    print("wrong user name or password")

            loop = False
        else:
            print("Username does not exist")
    except IndexError:
        print('User Does not Exist.')

    cnx.close()


def begin():
    print("Welcome to Helix AI")


if granted:
    print("Welcome to Helix AI")
    print("### USER DETAILS ###")
    print("Username: ", name)
