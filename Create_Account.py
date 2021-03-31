import PySimpleGUI as sg
import Main as ms
import Login as lg
import pyodbc
import Validations as vl
import base64

database = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                          'Server= MICHAEL-PC\SQLSSIS;'
                          'Database=Python_DB;'
                          'Trusted_Connection=yes;')

cursor = database.cursor()


# finish password confirmation
# pop to show that account has been created, possibly ask if they want to login
# sg.preview_all_look_and_feel_themes()

def username_check(username):
    username_validation = vl.username_validation(username)

    if username_validation == -1:
        sg.popup_error('Username Error', 'Your username must have more 6 but less than 15 characters')
    elif username_validation == -2:
        sg.popup_error('Username Error', 'That username is in use, please try another one')

    return 0


def password_check(password, password2=''):
    password_validation = vl.password_validation(password, password2)
    print(password2)

    if password_validation == -3:
        sg.popup_error('Password Error', 'Your password has to have more than 6 characters')
    elif password_validation == -4:
        sg.popup_error('Password Error', 'Your password has to contain a uppercase character')
    elif password_validation == -5:
        sg.popup_error('Password Error', 'Your password has to contain a lowercase character')
    elif password_validation == -6:
        sg.popup_error('Password Error', 'Your password has to contain a number')
    elif password_validation == -7:
        sg.popup_error('Password Error', 'Your password has to contain a special character($#@!)')
    elif password_validation == -8:
        sg.popup_error('Password Error', 'Your password must match')
    return 0


def password_encode(password):
    # Encoding password in base64
    password_encode_value = base64.b64encode(password.encode('UTF-8'))
    return password_encode_value.decode()


def account_creation(username, password_encoded_val, f_name, l_name):
    # Creating user details on the database

    cursor.execute("insert into dbo.Reminder_users(Username, PasswordEncode, FirstName, LastName) values(?, "
                   "?, ?, ?)",
                   username, password_encoded_val, f_name, l_name)

    database.commit()

    return  True

def main():
    # setting a theme
    sg.theme('DarkBlue1')
    button_font = ('Sans', 15)
    text_font = ('Sans', 15)
    entry_field_size = (30, 5)

    # setting a layout
    layout = [
        # each list within this list can be seen a line on the gui
        [sg.Button('Back', font=button_font),
         sg.Text('Create Account', font=('Sans', 20), size=(1000, 1), justification='c')],
        [sg.Text('')],
        # Set keys to access/update the field later
        [sg.Text('Username', font=text_font, size=(9, 1)), sg.Input(key='-USERNAME-', size=entry_field_size)],
        [sg.Text('Password', font=text_font, size=(9, 1)),
         sg.Input(key='-PASSWORD-', password_char='*', size=entry_field_size)],
        [sg.Text('Confirm Password', font=text_font, size=(9, 1)),
         sg.Input(key='-PASSWORD2-', password_char='*', size=entry_field_size)],
        [sg.Text('First name', font=text_font, size=(9, 1)), sg.Input(key='-FIRSTNAME-', size=entry_field_size)],
        [sg.Text('Last name', font=text_font, size=(9, 1)), sg.Input(key='-LASTNAME-', size=entry_field_size)],
        [sg.Text('')],
        [sg.Button('Create', font=text_font, size=(15, 1))]
    ]

    # Window is required to display the layout
    window = sg.Window("Create Account", layout, size=(450, 350), grab_anywhere=True, element_justification='C')

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == 'Back':
            window.close()
            ms.main()

        if event == 'Create':
            # checking the username and password
            username_val_check = username_check(values['-USERNAME-'])
            password_val_check = password_check(values['-PASSWORD-'], values['-PASSWORD2-'])

            first_name_check = len(values['-FIRSTNAME-'])
            last_name_check = len(values['-LASTNAME-'])

            if first_name_check == 0:
                sg.popup_error('Empty field', 'Your name cannot be empty')
            elif last_name_check == 0:
                sg.popup_error('Empty field', 'Your password cannot be empty')

            if (username_val_check == 0 and password_val_check == 0) and (
                    first_name_check > 0 and last_name_check > 0):
                password_encoded_value = password_encode(values['-PASSWORD-'])
                username = values['-USERNAME-']

                ac_sucess = account_creation(username, password_encoded_value, values['-FIRSTNAME-'], values['-LASTNAME-'])

                if ac_sucess:
                    window.FindElement('-USERNAME-').Update('')
                    window.FindElement('-PASSWORD-').Update('')
                    window.FindElement('-PASSWORD2-').Update('')
                    window.FindElement('-FIRSTNAME-').Update('')
                    window.FindElement('-LASTNAME-').Update('')
                    ans = sg.popup_ok("Your account has been successfully created")
                    if ans == 'OK':
                        window.close()
                        lg.main()




if __name__ == '__main__':
    main()
