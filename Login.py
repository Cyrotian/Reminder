import PySimpleGUI as sg
import Main as ms
import pyodbc
import base64
import Display_Reminders as dr
import validators as VL

database = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                          'Server= MICHAEL-PC\SQLSSIS;'
                          'Database=Python_DB;'
                          'Trusted_Connection=yes;')

cursor = database.cursor()


# sg.preview_all_look_and_feel_themes()
#UPDATE ALL REMINDERS SET ACTIOVE USER TO 1 IF LOGIN IS SUCESSFULL
def login(username, password):
    db_password = base64.b64encode(password.encode('UTF-8')).decode()
    cursor.execute("Select Username FROM Python_DB.dbo.Reminder_users WHERE Username = ? and PasswordEncode = ? ",
                   username, db_password)

    result = len([username for values in cursor])

    if result == 1:
        return True
    else:
        sg.popup_error("Failed Login", "Your username or password is incorrect, please try again")
        return False


def main():
    sg.theme('DarkBlue1')
    entry_field_size = (30, 5)

    button_font = ('Sans', 15)
    text_font = ('Sans', 15)
    layout = [
        [sg.Button('Back', font=button_font), sg.Text('Login', font=('Sans', 30), size=(1000, 1), justification='c')],
        [sg.Text('')],
        [sg.Text('Username', font=text_font), sg.Input(key='-USERNAME-', size=entry_field_size)],
        [sg.Text('Password', font=text_font), sg.Input(key='-PASSWORD-', password_char='*', size=entry_field_size)],
        [sg.Text('')],
        [sg.Button('Login', font=text_font, size=(15, 1))]
    ]
    window = sg.Window("login", layout, size=(300, 250), grab_anywhere=True, element_justification='C')

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == 'Back':
            window.close()
            ms.main()

        if event == 'Login':

            login_check = bool(login(values['-USERNAME-'], values['-PASSWORD-']))
            if login_check:
                window.close()
                dr.main(current_user=values['-USERNAME-'])
            else:
                window.FindElement('-USERNAME-').Update('')
                window.FindElement('-PASSWORD-').Update('')



if __name__ == '__main__':
    main()
