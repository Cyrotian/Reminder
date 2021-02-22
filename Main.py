import PySimpleGUI as sg
import Theme as th


def main():
    sg.LOOK_AND_FEEL_TABLE['ReminderTheme'] = {'BACKGROUND': '#3c94c3',
                                               'TEXT': '#3CC36B',
                                               'INPUT': '#1BC1E4',
                                               'TEXT_INPUT': '#000000',
                                               'SCROLL': '# 99CC99',
                                               'BUTTON': ('#E4471B', '#3CC3AE'),
                                               'PROGRESS': ('# D1826B', '# CC8019'),
                                               'BORDER': 1, 'SLIDER_DEPTH': 0,
                                               'PROGRESS_DEPTH': 0, }
    sg.theme('ReminderTheme')

    layout = [
        [sg.Text('Reminder', justification='center', size=(1000, 1), font='Sans')],

        [sg.Button('Login', font='Sans'),
         sg.Button('Create Account', font='Sans'),
         sg.Button('Exit', font='Sans')]
    ]

    window = sg.Window('Reminder', layout, size=(500, 150), grab_anywhere=True, element_justification='c')

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break


if __name__ == '__main__':
    main()
