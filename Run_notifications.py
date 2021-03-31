from win10toast import ToastNotifier
from plyer import notification
import pyodbc
import datetime as dt
import time


# add leeway to time + 3 minutes (sleep  for 3 mintues) time.sleep(seconds)
database = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                          'Server= MICHAEL-PC\SQLSSIS;'
                          'Database=Python_DB;'
                          'Trusted_Connection=yes;')

cursor = database.cursor()


def update_lastrun(reminder_id):
    cursor.execute("Update Reminders SET last_run = CAST(Getdate()AS DATE) where id = ?", reminder_id)
    cursor.commit()


def get_runtime(title, message, freq_type, freq_int, start_date, last_run, reminder_time, id):
    # getting the time in "H:M" format
    current_date = dt.datetime.now().date()
    current_time = dt.datetime.now().time().strftime("%H:%M:00")

    # adding frequency interval to the last run to determine if this reminder is supposed to run today
    # if the reminder has run previously then use the last_run date
    if last_run is not None:
        current_run = last_run + dt.timedelta(days=freq_int)
        # checking if the date and the time match up to show the notification
        if current_run == current_date and current_time == str(reminder_time):
            run_notification(title, message)
            update_lastrun(id)

    else:
        # if the reminder hasn't run before than use the start date
        if start_date == current_date and current_time == str(reminder_time):
            run_notification(title, message)
            update_lastrun(id)

    # if start_date or current_run == dt.datetime.now().date():
    #   run_notification(title, message)


def run_notification(title, message):
    toast = ToastNotifier()
    toast.show_toast(
        title=title,
        msg=message,
        duration=7,
        icon_path='I:\\Phyton\\desktop_reminder\\reminder_icon.ico'
    )
    # notification.notify(
    #     title=str(title),
    #     message=str(message),
    #     app_icon=None,  # e.g. 'C:\\icon_32x32.ico'
    #     timeout=5,  # seconds
    # )
    time.sleep(1)


def main():
    # Getting reminders that are supposed to run on the current day
    active_user_notifications = cursor.execute("Select id, Title, Message, frequency_type,frequency_interval, "
                                               "start_date, Last_run, Reminder_time from dbo.reminders where "
                                               "active_user = 1 and ((Start_date = cast(GETDATE() as date) or ("
                                               "DATEADD(DD, Frequency_interval, Last_run)= cast(GETDATE()as date))))").fetchall()

    for i in range(len(active_user_notifications)):
        notification_values = []
        id = active_user_notifications[i][0]
        for j in range(len(active_user_notifications[i])):
            if j == 2:
                notification_values.append(active_user_notifications[i][j].strip())
            else:
                notification_values.append(active_user_notifications[i][j])
        # assigning values in notifications values into variables starting at position 1

        title, message, freq_type, freq_int, start_date, last_run, reminder_time = [notification_values[i] for i in
                                                                                    range(1, len(notification_values))]

        get_runtime(title, message, freq_type, freq_int, start_date, last_run, reminder_time, id)


if __name__ == '__main__':
    main()
    cursor.close()
