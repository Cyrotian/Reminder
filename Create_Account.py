import PySimpleGUI as SG
import Main as MS
import pyodbc
import hashlib
import Validations as VL
import base64

database = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                          'Server= MICHAEL-PC\SQLSSIS;'
                          'Database=Python_DB;'
                          'Trusted_Connection=yes;')

cursor = database.cursor()


# sg.preview_all_look_and_feel_themes()

def username_check(username):
    username_validation = VL.username_validation(username)

    if username_validation == -1:
        SG.popup_error('Username Error', 'Your username must have more 6 but less than 15 characters')
    elif username_validation == -2:
        SG.popup_error('Username Error', 'That username is in use, please try another one')

    return 0


def password_check(password):
    password_validation = VL.password_validation(password)
    print(password_validation)

    if password_validation == -3:
        SG.popup_error('Password Error', 'Your password has to have more than 6 characters')
    elif password_validation == -4:
        SG.popup_error('Password Error', 'YYour password has to contain a uppercase character')
    elif password_validation == -5:
        SG.popup_error('Password Error', 'Your password has to contain a lowercase character')
    elif password_validation == -6:
        SG.popup_error('Password Error', 'Your password has to contain a number')
    elif password_validation == -7:
        SG.popup_error('Password Error', 'Your password has to contain a special character($#@!)')

    return 0


def password_encode(password):

    password_encode_value = base64.b64encode(password.encode('UTF-8'))
    return password_encode_value.decode()


def account_creation(username, password_encoded_val, f_name, l_name):
    # password_bytes = password_hash_val.encode('ascii')
    # b64_bytes = b64.b64encode(password_bytes)

    print(f'username in account creation = {username} \n Hash value = {password_encoded_val}')
    print(type(password_encoded_val))

    cursor.execute("insert into dbo.User_Reminder(Username, PasswordEncode, FirstName, LastName) values(?, "
                   "?, ?, ?)",
                   username, password_encoded_val, f_name, l_name)

    database.commit()

    # print(b64.decodebytes(b641))


def main():
    # setting a theme
    SG.theme('DarkBlue1')
    button_font = ('Sans', 15)
    text_font = ('Sans', 15)

    # setting a layout
    layout = [
        # each list within this list can be seen a line on the gui
        [SG.Button('Back', font=button_font),
         SG.Text('Create Account', font=('Sans', 20), size=(1000, 1), justification='c')],
        [SG.Text('')],
        # Set keys to access/update the field later
        [SG.Text('Username', font=text_font, size=(9, 1)), SG.Input(key='-USERNAME-', size=(30, 5))],
        [SG.Text('Password', font=text_font, size=(9, 1)), SG.Input(key='-PASSWORD-', password_char='*', size=(30, 5))],
        [SG.Text('First name', font=text_font, size=(9, 1)), SG.Input(key='-FIRSTNAME-', size=(30, 5))],
        [SG.Text('Last name', font=text_font, size=(9, 1)), SG.Input(key='-LASTNAME-', size=(30, 5))],
        [SG.Text('')],
        [SG.Button('Create', font=text_font, size=(15, 1))]
    ]

    # Window is required to display the layout
    window = SG.Window("Create Account", layout, size=(300, 300), grab_anywhere=True, element_justification='C')

    while True:
        event, values = window.read()
        if event == "Exit" or event == SG.WIN_CLOSED:
            break
        if event == 'Back':
            window.close()
            MS.main()

        if event == 'Create':
            # checking the username
            username_val_check = username_check(values['-USERNAME-'])
            password_val_check = password_check(values['-PASSWORD-'])

            first_name_check = len(values['-FIRSTNAME-'])
            last_name_check = len(values['-LASTNAME-'])

            if first_name_check == 0:
                SG.popup_error('Empty field', 'Your name cannot be empty')
            elif last_name_check == 0:
                SG.popup_error('Empty field', 'Your password cannot be empty')

            if (username_val_check == 0 and password_val_check == 0) and (
                    first_name_check > 0 and last_name_check > 0):
                password_encoded_value = password_encode(values['-PASSWORD-'])
                username = values['-USERNAME-']

                account_creation(username, password_encoded_value, values['-FIRSTNAME-'], values['-LASTNAME-'])

                window.FindElement('-USERNAME-').Update('')
                window.FindElement('-PASSWORD-').Update('')
                window.FindElement('-FIRSTNAME-').Update('')
                window.FindElement('-LASTNAME-').Update('')

                # sg.popup('Account Created', 'Your')

            # insert hash value into DB - work out why Hash value is not working
            # Loop to ensure that code doesn't insert on error
            # Clear DB


if __name__ == '__main__':
    main()