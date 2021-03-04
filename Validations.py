import re
import pyodbc

database = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                          'Server= MICHAEL-PC\SQLSSIS;'
                          'Database=Python_DB;'
                          'Trusted_Connection=yes;')

cursor = database.cursor()


def username_validation(username):
    if len(username) < 6 or len(username) > 15:
        return -1
    cursor.execute("Select Username FROM Python_DB.dbo.Reminder_users WHERE Username = ?", username)

    user_count = 0
    for row in cursor:
        user_count = len(row)
        break
    if user_count > 0:
        return -2

    return 0


def password_validation(password):
    if len(password) < 6:
        return -3
    # Using re.search to find the values expected in a password
    elif not re.search("[A-Z]", password):
        return -4
    elif not re.search("[a-z]", password):
        return -5
    elif not re.search("[0-9]", password):
        return -6
    elif not re.search("[$#@!]", password):
        return -7

    return 0
