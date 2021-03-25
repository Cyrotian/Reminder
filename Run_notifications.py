from win10toast import ToastNotifier
from plyer import notification
import pyodbc
import datetime as dt
import time

# toast = ToastNotifier()
# toast.show_toast("alert","text")

# get list of reminders for active users
# check the frequency type
# if this equals once- check the reminder time and start date
# if start date is in the past ignore
# else check the last run date
# if the last run time is null, check if adding the start_date to the interval equals today
# if it does equal today, check the reminder time
# if it doesn't equal today ignore
# if the reminder time is past the current time(pc was turn on later so reminder didn't run)
# and it's not frequency type - once , update last run to equal today.
# if the reminder time is still a time in the future - add title and message to list
# use the time module to check if the time matches,if it does pass title and message to notification, show notiication
# add leeway to time + 3 minutes (sleep  for 3 mintues) time.sleep(seconds)
database = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                          'Server= MICHAEL-PC\SQLSSIS;'
                          'Database=Python_DB;'
                          'Trusted_Connection=yes;')

cursor = database.cursor()


def update_lastrun(reminder_id, date):
    pass


def run_notification(title, message):
    notification.notify(
        title=str(title),
        message=str(message),
        app_icon=None,  # e.g. 'C:\\icon_32x32.ico'
        timeout=3,  # seconds
    )


def main():
    active_user_notifications = cursor.execute("Select User_id, Title, Message, frequency_type"
                                               ", frequency_interval, start_date, Last_run, Reminder_time"
                                               " from dbo.reminders where active_user = 1 ").fetchall()

    # frequency_type = 3
    # frequency_interval = 4

    # title, message, freq_type, freq_int, start_date, last_run, reminder_time = ['', '', '', '', '', '', '']

    for i in range(len(active_user_notifications)):
        notification_values = []
        for j in range(len(active_user_notifications[i])):
            id = active_user_notifications[i][0]
            if j == 2:
                notification_values.append(active_user_notifications[i][j].strip())
            else:
                notification_values.append(active_user_notifications[i][j])

        title, message, freq_type, freq_int, start_date, last_run, reminder_time = [notification_values[i] for i in
                                                                                    range(1, len(notification_values))]
        # getting the time in "H:M" format
        current_time = dt.datetime.now().time().strftime("%H:%M")
        print(str(current_time.strip(':')))
        if current_time > str(reminder_time):
            pass
            #print(current_time + '' + reminder_time)
        if freq_type == 'Once':
            if start_date == dt.datetime.now().date():
                run_notification(title, message)

        # print(notification_values)


if __name__ == '__main__':
    main()
    cursor.close()
