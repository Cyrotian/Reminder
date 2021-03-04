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
    entry_field_size = (20, 5)

    button_font = ('Sans', 15)
    text_font = ('Sans', 15)
    layout = [
        [SG.Text('Add New Reminder', font=('Sans', 30), size=(1000, 1), justification='c')],
        [SG.Text('')],
        [SG.Text('Title', font=text_font), SG.Input(key='-TITLE-', size=entry_field_size)],
        [SG.Text('Message', font=text_font), SG.Multiline(key='-MESSAGE-', size=(30, 5))],
        [SG.Text('Frequency', font=text_font), SG.Combo(['Once', 'Daily', 'Weekly', 'Monthly', 'Annually'])],
        [SG.Text('Start Date', font=text_font), SG.Input(key='-DATE-', size=entry_field_size,
                                                         readonly=True, background_color='brown'),
         SG.CalendarButton('Select Date', target='-DATE-', format='%d/%m/%Y')],
        [SG.Button('Create New', font=text_font, size=(15, 1))]
    ]
    window = SG.Window("Reminders", layout, size=(500, 500), grab_anywhere=True, element_justification='C')

    while True:
        event, values = window.read()
        if event == SG.WIN_CLOSED:
            break

        if event == 'Create New':
            SG.Popup(kwargs.get('current_user', None))
            print(values['-DATE-'])

        if event == 'Logout':
            window.close()
            MS.main()


if __name__ == '__main__':
    main()
    # call main from login like this: main(name  = username)
