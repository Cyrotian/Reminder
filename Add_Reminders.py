import PySimpleGUI as sg
import Main as ms
import Display_Reminders as DR
import pyodbc
import datetime as dt

database = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                          'Server= MICHAEL-PC\SQLSSIS;'
                          'Database=Python_DB;'
                          'Trusted_Connection=yes;')

cursor = database.cursor()


# Screen layout - Pad
# reduce message box field size

def db_insert(username, title, message, frequency, start_date, reminder_time, interval):
    # selecting the user id from the database, this returns a list of tuples
    user = cursor.execute("SELECT UserID from dbo.Reminder_users WHERE Username = ? ", username).fetchall()
    # getting the actual user_id from the list of tuple
    user_id = user[0][0]
    # adding the data into the database table
    # converting start date from dd-mm-yyyy to yyyy-mm-dd for db insert
    start_date = dt.datetime.strptime(start_date, '%d-%m-%Y').isoformat()

    cursor.execute("Insert into dbo.Reminders(User_id, Title, Message, Frequency_type, Frequency_interval, "
                   "Start_date, Reminder_time, Active_user) "
                   "values(?,?,?,?,?,?,?,?)", user_id, title, message, frequency,
                   interval, start_date, reminder_time, 1)

    # updating the fields to ensure that only the user logged in has an active reminder
    cursor.execute("Update dbo.Reminders set Active_user = 1 where User_id = ?", user_id)
    cursor.execute("Update dbo.Reminders set Active_user = 0 where User_id != ?", user_id)

    # committing the changes
    database.commit()


def main(**kwargs):
    sg.theme('DarkBlue1')
    entry_field_size = (20, 5)
    button_font = ('Sans', 15)
    text_font = ('Sans', 15)
    layout = [
        [sg.Text('Add New Reminder', font=('Sans', 30), size=(1000, 1), justification='c')],

        [sg.Text('')],
        [sg.Text('Title', font=text_font), sg.Input(key='-TITLE-', size=entry_field_size)],
        [sg.Text('Message', font=text_font), sg.Multiline(key='-MESSAGE-', size=(20, 2))],
        [sg.Text('Frequency', font=text_font), sg.Combo(['Once', 'Daily', 'Weekly', 'Monthly', 'Annually'],
                                                        readonly=True, key='-FREQ-')],
        [sg.Text('Start Date', font=text_font), sg.Input(key='-DATE-', size=entry_field_size,
                                                         readonly=True, text_color='black'),
         sg.CalendarButton('Select Date', target='-DATE-', format='%d-%m-%Y')],
        # list of times
        [sg.Text('Time(24Hr Clock)', font=text_font), sg.Combo([
            '00:00', '00:30', '01:00', '01:30', '02:00', '02:30', '03:00', '03:30', '04:00', '04:30', '05:00', '05:30',
            '06:00', '06:30', '07:00', '07:30', '08:00', '08:30', '09:00', '09:30', '10:00', '10:30', '11:00', '11:30',
            '12:00', '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30',
            '18:00', '18:30', '19:00', '19:30', '20:00', '20:30', '21:00', '21:30', '22:00', '22:30', '23:00', '23:30'
        ], key='-TIME-', readonly=True)],

        [sg.Button('Create New', font=text_font, size=(15, 1))]
    ]
    window = sg.Window("Reminders", layout, size=(500, 350), element_justification='C')

    while True:
        event, values = window.read()
        inserted_data = []

        if event == sg.WIN_CLOSED:
            break

        if event == 'Create New':
            # Getting the current user passed from Display reminders
            current_user = kwargs.get('user', None)
            title = values['-TITLE-']
            message = values['-MESSAGE-']
            freq = values['-FREQ-']
            date = values['-DATE-']
            time = values['-TIME-']
            interval = 0

            # setting the interval based on the frequency
            if freq == 'Once':
                interval = 0
            elif freq == 'Daily':
                interval = 1
            elif freq == 'Weekly':
                interval = 7
            elif freq == 'Monthly':
                interval = 31
            elif freq == 'Annually':
                interval = 365

            # adding the variables to the inserted data list using extends
            inserted_data.extend([title, message, freq, date, time])
            is_error = False

            # error field to show which field is empty
            error_field = ''
            for i in range(len(inserted_data)):
                if i == 0:
                    error_field = 'Title'
                elif i == 1:
                    error_field = 'Message'
                elif i == 2:
                    error_field = 'Frequency'
                elif i == 3:
                    error_field = 'Date'
                elif i == 4:
                    error_field = 'Time'

                # when message field is empty it has \n as the default value
                if inserted_data[i] == '' or inserted_data[i] == '\n':
                    sg.PopupError('Empty Field', f'{error_field} field cannot be empty')
                    is_error = True
                    break
            # if there are no errors pass the variables to be inserted
            if not is_error:
                db_insert(current_user, title, message, freq, date, time, interval)
                # getting window from display reminders and passing it back into display reminders
                DR.update_table(current_user=current_user, window=kwargs.get('window'))
                window.close()

        if event == 'Logout':
            window.close()
            ms.main()


if __name__ == '__main__':
    main()
    cursor.close()
    # call main from login like this: main(name  = username)
