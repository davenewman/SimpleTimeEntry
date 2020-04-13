import PySimpleGUI as sg
import os

def find_file():

    sg.theme('Dark Blue')
    
    layout = [  [sg.Text(f'No database file was found in the directory this script resides in.')],
                [sg.Text(f'Current working directory: {os.getcwd()}')],
                [sg.Text('Find database file')],
                [sg.Input(), sg.FileBrowse()],
                [sg.OK(), sg.Cancel(), sg.Button('Create new database')]  ]
    
    window = sg.Window('Find database file', layout)

    event, values = window.read()
    window.close()
    
    return event, values


def db_error_popup():

    sg.theme('Dark Blue')

    layout = [  [sg.Text('Exiting program.')],
                [sg.Text("Database file must end in '.db'")],
                [sg.OK()]  ]

    window = sg.Window('Unable to find database file', layout)
    event, values = window.read()
    window.close()

if __name__ == "__main__":

    event, values = find_file()
    print(f"event = {event}")
    print(f"values = {values}")

    db_error_popup()
    

    
