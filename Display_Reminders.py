import PySimpleGUI as SG
import Main as MS
import pyodbc
from Add_Reminders import main as AR

database = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                          'Server= MICHAEL-PC\SQLSSIS;'
                          'Database=Python_DB;'
                          'Trusted_Connection=yes;')

cursor = database.cursor()


def main(**kwargs):
    # current_user = kwargs.get('current_user', None)
    current_user = 'cryola'
    SG.theme('DarkBlue1')
    entry_field_size = (30, 5)

    button_font = ('Sans', 15)
    text_font = ('Sans', 15)
    #change start date to last run
    #update table when user creates new reminder
    #add delete icon
    reminders = cursor.execute("Select Title, Message, Frequency_type, CONVERT(varchar(10),Start_date, 103) AS 'Start "
                               "Date', Reminder_time from dbo.Reminders "
                               "as r INNER JOIN dbo.Reminder_users as ru on r.User_id = "
                               "ru.UserID WHERE ru.Username = ? ", current_user).fetchall()
    # header for the table
    header_list = ['Title', 'Message', 'Frequency', 'Start Date', 'Reminder Time']

    reminder_list = [list(row) for row in reminders]

    layout = [
        [SG.Button('Logout', font=button_font),
         SG.Text('Reminders', font=('Sans', 30), size=(1000, 1), justification='c')],
        [SG.Text('')],
        [SG.Table(values=list(reminder_list), headings=header_list, display_row_numbers=True, justification='c',
                  auto_size_columns=True,row_height=25 ,max_col_width=10, key='-TABLE-')],

        [SG.Text('')],
        [SG.Button('Create New', font=text_font, size=(15, 1))]

    ]
    window = SG.Window("Reminders", layout, size=(500, 500), element_justification='C')

    while True:
        event, values = window.read()
        if event == SG.WIN_CLOSED:
            break

        if event == 'Create New':
            # SG.Popup(kwargs.get('current_user', None))
            AR(user=current_user)

        if event == 'Logout':
            window.close()
            MS.main()


if __name__ == '__main__':
    main()
    # call main from login like this: main(name  = username)
