import PySimpleGUI as sg
import Main as ms
import pyodbc
import hashlib
import Validations as vl
import base64 as b64
database = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                          'Server= MICHAEL-PC\SQLSSIS;'
                          'Database=Python_DB;'
                          'Trusted_Connection=yes;')

cursor = database.cursor()


# sg.preview_all_look_and_feel_themes()

def username_check(username):
    username_validation = vl.username_validation(username)

    if username_validation == -1:
        sg.popup_error('Username Error', 'Your username must have more 6 but less than 15 characters')
    elif username_validation == -2:
        sg.popup_error('Username Error', 'That username is in use, please try another one')

    return 0


def password_check(password):
    password_validation = vl.password_validation(password)
    print(password_validation)

    if password_validation == -3:
        sg.popup_error('Password Error', 'Your password has to have more than 6 characters')
    elif password_validation == -4:
        sg.popup_error('Password Error', 'YYour password has to contain a uppercase character')
    elif password_validation == -5:
        sg.popup_error('Password Error', 'Your password has to contain a lowercase character')
    elif password_validation == -6:
        sg.popup_error('Password Error', 'Your password has to contain a number')
    elif password_validation == -7:
        sg.popup_error('Password Error', 'Your password has to contain a special character($#@!)')

    return 0


def password_hash(password):
    try:
        hash_val = hashlib.sha1()
        hash_val.update(password.encode('utf-8'))
        password_hash = hash_val.hexdigest()
        return password_hash
    except:
        sg.popup_error('Hashing Error', 'Unable to hash password, please try again later')


def account_creation(username, password_hash_val, f_name, l_name):
    password_bytes = password_hash_val.encode('ascii')
    b64_bytes = b64.b64encode(password_bytes)

    print(f'username in account creation = {username} \n Hash value = {password_hash_val}')
    print(type(password_hash_val))
    print(f'base 64 value = {b64.encodebytes(b64_bytes)}')
    print(f'base 64 ascii = {b64.encodebytes(b64_bytes).decode("ascii")}')
    b641 = b64.encodebytes(b64_bytes)
    b642 = b64.encodebytes(b64_bytes).decode("ascii")
    cursor.execute("insert into dbo.User_Reminder(Username, PasswordHash, FirstName, LastName) values(?, "
                   "? ?, ?)",
                   username, b642, f_name, l_name)

    database.commit()

    ## fix error


def main():
    # setting a theme
    sg.theme('DarkBlue1')

    button_font = ('Sans', 15)
    text_font = ('Sans', 15)
    # setting a layout
    layout = [
        # each list within this list can be seen a line on the gui
        [sg.Button('Back', font=button_font),
         sg.Text('Create Account', font=('Sans', 20), size=(1000, 1), justification='c')],
        # Set keys to access/update the field later
        [sg.Text('Username', font=text_font), sg.Input(key='-USERNAME-')],
        [sg.Text('Password', font=text_font), sg.Input(key='-PASSWORD-', password_char='*')],
        [sg.Text('First name', font=text_font), sg.Input(key='-FIRSTNAME-')],
        [sg.Text('Last name', font=text_font), sg.Input(key='-LASTNAME-')],
        [sg.Button('Create', font=text_font)]
    ]

    # Window is required to display the layout
    window = sg.Window("Create Account", layout, size=(300, 300), grab_anywhere=True, element_justification='C')

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == 'Back':
            window.close()
            ms.main()

        if event == 'Create':
            # checking the username
            username_val_check = username_check(values['-USERNAME-'])
            password_val_check = password_check(values['-PASSWORD-'])

            first_name_check = len(values['-FIRSTNAME-'])
            first_name = values['-FIRSTNAME-']

            if first_name_check == 0 or len(first_name) == 0:
                sg.popup_error('Empty field', 'Your name cannot be empty')

            last_name_check = len(values['-LASTNAME-'])
            last_name = values['-LASTNAME-']

            if last_name_check == 0:
                sg.popup_error('Empty field', 'Your password cannot be empty')

            if (username_val_check == 0 and password_val_check == 0) and (
                    first_name_check > 0 and last_name_check > 0):
                password_hash_value = password_hash(values['-PASSWORD-'])
                username = values['-USERNAME-']

                account_creation(username, password_hash_value, first_name, last_name)

                window.FindElement('-USERNAME-').Update('')
                window.FindElement('-PASSWORD-').Update('')
                window.FindElement('-FIRSTNAME-').Update('')
                window.FindElement('-LASTNAME-').Update('')

                # sg.popup('Account Created', 'Your')

            # insert hash value into DB


if __name__ == '__main__':
    main()
