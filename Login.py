import PySimpleGUI as SG
import Main as MS
import pyodbc
import base64
import Display_Reminders as DR
import validators as VL

database = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                          'Server= MICHAEL-PC\SQLSSIS;'
                          'Database=Python_DB;'
                          'Trusted_Connection=yes;')

cursor = database.cursor()


# sg.preview_all_look_and_feel_themes()
def login(username, password):
    db_password = base64.b64encode(password.encode('UTF-8')).decode()
    cursor.execute("Select Username FROM Python_DB.dbo.Reminder_users WHERE Username = ? and PasswordEncode = ? ",
                   username, db_password)

    result = len([username for values in cursor])

    if result == 1:
        SG.popup_ok("Success", "it works")
        return True
    else:
        SG.popup_error("Failed Login", "Your username or password is incorrect, please try again")
        return False


def main():
    SG.theme('DarkBlue1')
    entry_field_size = (30, 5)

    button_font = ('Sans', 15)
    text_font = ('Sans', 15)
    layout = [
        [SG.Button('Back', font=button_font), SG.Text('Login', font=('Sans', 30), size=(1000, 1), justification='c')],
        [SG.Text('')],
        [SG.Text('Username', font=text_font), SG.Input(key='-USERNAME-', size=entry_field_size)],
        [SG.Text('Password', font=text_font), SG.Input(key='-PASSWORD-', password_char='*', size=entry_field_size)],
        [SG.Text('')],
        [SG.Button('Login', font=text_font, size=(15, 1))]
    ]
    window = SG.Window("login", layout, size=(300, 250), grab_anywhere=True, element_justification='C')

    while True:
        event, values = window.read()
        if event == "Exit" or event == SG.WIN_CLOSED:
            break
        if event == 'Back':
            window.close()
            MS.main()

        if event == 'Login':

            login_check = bool(login(values['-USERNAME-'], values['-PASSWORD-']))
            if login_check:
                window.close()
                DR.main(current_user=values['-USERNAME-'])
            else:
                print("Failure")
                window.FindElement('-USERNAME-').Update('')
                window.FindElement('-PASSWORD-').Update('')



if __name__ == '__main__':
    main()
