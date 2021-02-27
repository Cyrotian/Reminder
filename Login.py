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
    sg.theme('DarkBlue1')
    username = ''
    password = ''
    button_font = ('Sans', 15)
    text_font = ('Sans', 15)
    layout = [
        [sg.Button('Back', font=button_font), sg.Text('Login', font=('Sans', 30), size=(1000, 1), justification='c')],
        [sg.Text('')],
        [sg.Text('Username', font=text_font), sg.Input(key='-USERNAME-')],
        [sg.Text('Password', font=text_font), sg.Input(key='-PASSWORD-', password_char='*')],
        [sg.Text('')],
        [sg.Button('Login', font=text_font, size=(15, 1))]
    ]
    window = sg.Window("login", layout, size=(300,250), grab_anywhere=True, element_justification='C')

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
            #check hash value agaist db
if __name__ == '__main__':
    main()
