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
        [SG.Text('Frequency', font=text_font), SG.Combo(['Once', 'Daily', 'Weekly', 'Monthly', 'Annually'],
                                                        readonly=True, key='-FREQ-')],
        [SG.Text('Start Date', font=text_font), SG.Input(key='-DATE-', size=entry_field_size,
                                                         readonly=True, text_color='red'),
         SG.CalendarButton('Select Date', target='-DATE-', format='%d-%m-%Y')],

        [SG.Text('Time(24Hr Clock)', font=text_font), SG.Combo([
            '00:00',
            '00:30',
            '01:00',
            '01:30',
            '02:00',
            '02:30',
            '03:00',
            '03:30',
            '04:00',
            '04:30',
            '05:00',
            '05:30',
            '06:00',
            '06:30',
            '07:00',
            '07:30',
            '08:00',
            '08:30',
            '09:00',
            '09:30',
            '10:00',
            '10:30',
            '11:00',
            '11:30',
            '12:00',
            '12:30',
            '13:00',
            '13:30',
            '14:00',
            '14:30',
            '15:00',
            '15:30',
            '16:00',
            '16:30',
            '17:00',
            '17:30',
            '18:00',
            '18:30',
            '19:00',
            '19:30',
            '20:00',
            '20:30',
            '21:00',
            '21:30',
            '22:00',
            '22:30',
            '23:00',
            '23:30'
        ], key='-TIME-', readonly=True)],

        [SG.Button('Create New', font=text_font, size=(15, 1))]
    ]
    window = SG.Window("Reminders", layout, size=(500, 500), element_justification='C')

    while True:
        event, values = window.read()
        inserted_data = []

        if event == SG.WIN_CLOSED:
            break

        if event == 'Create New':
            SG.Popup(kwargs.get('user', None))

            title = values['-TITLE-']
            message = values['-MESSAGE-']
            freq = values['-FREQ-']
            date = values['-DATE-']
            time = values['-TIME-']

            inserted_data.extend([title, message, freq, date, time])

            for value in inserted_data:
                if value == '':
                    SG.PopupError('Empty value', 'You cannot have an empty field')
                    break

        if event == 'Logout':
            window.close()
            MS.main()


if __name__ == '__main__':
    main()
    # call main from login like this: main(name  = username)
