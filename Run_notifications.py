from win10toast import ToastNotifier
from plyer import notification

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

notification.notify(
    title='Here is the title',
    message='Here is the message',
    app_icon=None,  # e.g. 'C:\\icon_32x32.ico'
    timeout=10,  # seconds
)
