import PySimpleGUI as sg
import Main as ms
import pyodbc
from Add_Reminders import main as ar

database = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                          'Server= MICHAEL-PC\SQLSSIS;'
                          'Database=Python_DB;'
                          'Trusted_Connection=yes;')

cursor = database.cursor()


# change start date to last run - use isnull to prevent errors
# show user first name on screen


def get_dbvalues(current_user):
    reminders = cursor.execute("Select Title, Message, Frequency_type, CONVERT(varchar(10),Start_date, 103) AS 'Start "
                               "Date', Reminder_time, id from dbo.Reminders "
                               "as r INNER JOIN dbo.Reminder_users as ru on r.User_id = "
                               "ru.UserID WHERE ru.Username = ? ", current_user).fetchall()
    return [list(row) for row in reminders]


def update_table(**kwargs):
    window = kwargs.get('window')
    current_user = kwargs.get('current_user')
    window.Element('-TABLE-').Update(values=get_dbvalues(current_user))


def delete_reminder(current_user, selected_row, reminder, window):
    # print(current_user, selected_row)
    db_id = reminder[selected_row][5]
    title = reminder[selected_row][0]

    confirm = sg.popup_yes_no('Confirm Delete', f'Are you sure you want to delete {title}', keep_on_top=True)
    if confirm == "Yes":
        cursor.execute("delete from dbo.Reminders where id = ?", db_id)
        database.commit()
        # passing window into add reminders so that table can be updated
        update_table(current_user=current_user, window=window)


def main(**kwargs):
    current_user = 'Mikko123'
    # kwargs.get('current_user')
    sg.theme('DarkBlue1')
    entry_field_size = (30, 5)

    button_font = ('Sans', 15)
    text_font = ('Sans', 15)

    # header for the table
    header_list = ['Title', 'Message', 'Frequency', 'Start Date', 'Reminder Time']

    reminder_list = get_dbvalues(current_user)
  #  if len(reminder_list) < 1:
        # list of empty values to display table it there are no reminders
    #    reminder_list = [['' for _ in range(len(header_list))]]

    layout = [
        [sg.Button('Logout', font=button_font),
         sg.Text('Reminders', font=('Sans', 30), size=(1000, 1), justification='c')],
        [sg.T('')],
        [sg.Table(values=reminder_list, headings=header_list,display_row_numbers=True, justification='c',
                  auto_size_columns=False, row_height=25, col_widths=[5], enable_events=True, key='-TABLE-')],
        [sg.T('')],
        [sg.Button('Delete Reminder', font=text_font, size=(15, 1))],
        [sg.T('')],
        [sg.Button('Create New', font=text_font, size=(15, 1))]

    ]
    window = sg.Window("Reminders", layout, size=(650, 550), element_justification='C')
    selected_row = -1

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        if event == 'Create New':
            ar(user=current_user, window=window)
            update_table(current_user=current_user, window=window)

        if event == 'Logout':
            window.close()
            ms.main()

        if event == '-TABLE-':
            selected_row = values['-TABLE-'][0]

        if event == 'Delete Reminder':
            if selected_row == -1:
                sg.PopupError('Select row', 'No row has been selected for deletion')
            else:
                reminder_list = get_dbvalues(current_user)
                delete_reminder(current_user, selected_row, reminder_list, window)

            # print(selected_row)
            # delete_reminder(current_user, selected_row)


if __name__ == '__main__':
    main()
    cursor.close()
