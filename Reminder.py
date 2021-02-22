import PySimpleGUI as sg

# Create the window
sg.theme('DarkAmber')

layout = [
    [sg.Text('Test')],
    [sg.Input(), sg.Input()],
    [sg.Button('Button'), sg.Button('Exit')]
]
window = sg.Window("Demo", layout, grab_anywhere=True)
# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    print(event, values)
    if event == "Button":
        for value in values:
            print(values.get(value))

    if event == "Exit" or event == sg.WIN_CLOSED:
        break

window.close()