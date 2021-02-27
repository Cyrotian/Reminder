import PySimpleGUI as sg
import Login as lg
import Create_Account as ca


def main():
    sg.theme('DarkBlue1')
    button_font_size = 20
    layout = [
        [sg.Text('Reminder', justification='center', size=(1000, 1), font=('Sans', 30))],
        [sg.Text('')],
        [sg.Button('Login', font=('Sans', 15), size=(15, 1))],
        [sg.Text('')],
        [sg.Button('Create Account', font=('Sans', 15), size=(15, 1))],
        [sg.Text('')],
        [sg.Button('Exit', font=('Sans', 15), size=(15, 1))]
    ]

    window = sg.Window('Reminder', layout, size=(300, 300), grab_anywhere=True, element_justification='c')

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        if event == "Login":
            window.close()
            lg.main()
            break

        if event == "Create Account":
            window.close()
            ca.main()
            break


if __name__ == '__main__':
    main()
