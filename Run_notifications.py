from win10toast import ToastNotifier
from plyer import notification


#toast = ToastNotifier()
#toast.show_toast("alert","text")

notification.notify(
    title='Here is the title',
    message='Here is the message',
    app_icon=None,  # e.g. 'C:\\icon_32x32.ico'
    timeout=10,  # seconds
)