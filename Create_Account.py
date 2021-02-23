import PySimpleGUI as sg
import Main as ms
import pyodbc
import hashlib

database = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                          'Server= MICHAEL-PC\SQLSSIS;'
                          'Database=Python_DB;'
                          'Trusted_Connection=yes;')

cursor = database.cursor()


# sg.preview_all_look_and_feel_themes()


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
        [sg.Button('Login', font=text_font)]
    ]

    # Window is required to display the layout
    window = sg.Window("Create Account", layout, size=(300, 170), grab_anywhere=True, element_justification='C')

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == 'Back':
            window.close()
            ms.main()

        if event == 'Login':
            try:
                password = values['-PASSWORD-']
                hash_val = hashlib.sha1()
                hash_val.update(password.encode('utf-8'))
                password_hash = hash_val.hexdigest()
                print(password_hash)
            except:
                sg.popup_error('Hashing Error', 'Unable to hash password, please try again later')

            #insert hash value into DB

if __name__ == '__main__':
    main()
