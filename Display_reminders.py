import PySimpleGUI as SG
import Main as MS
import pyodbc
import base64
import validators as VL

database = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                          'Server= MICHAEL-PC\SQLSSIS;'
                          'Database=Python_DB;'
                          'Trusted_Connection=yes;')

cursor = database.cursor()


def main(**kwargs):
    SG.theme('DarkBlue1')
    SG.theme('DarkBlue1')
    entry_field_size = (30, 5)

    button_font = ('Sans', 15)
    text_font = ('Sans', 15)
    layout = [
        [SG.Button('Back', font=button_font),
         SG.Text('Reminders', font=('Sans', 30), size=(1000, 1), justification='c')],
        [SG.Text('')],

        [SG.Text('')],
        [SG.Button('Create New', font=text_font, size=(15, 1))]
    ]
    window = SG.Window("Reminders", layout, size=(500, 500), grab_anywhere=True, element_justification='C')

    while True:
        event, values = window.read()
        if event == SG.WIN_CLOSED:
            break

        if event == 'Create New':
            SG.Popup(kwargs.get('current_user', None))


if __name__ == '__main__':
    main()
    # call main from login like this: main(name  = username)
