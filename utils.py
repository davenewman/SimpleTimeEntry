import PySimpleGUI as sg

def find_file():

    sg.theme('Dark Blue')
    
    layout = [  [sg.Text('Filename')],
                [sg.Input(), sg.FileBrowse()],
                [sg.OK(), sg.Cancel()]  ]
    
    window = sg.Window('Find database file', layout)

    event, values = window.read()
    window.close()

    return event, values
