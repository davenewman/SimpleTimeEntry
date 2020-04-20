import PySimpleGUI as sg
import os


def find_file():
    sg.theme('Dark Blue')

    layout = [[sg.Text(f'No database file was found in the directory this script resides in.')],
              [sg.Text(f'Current working directory: {os.getcwd()}')],
              [sg.Text('Find database file')],
              [sg.Input(), sg.FileBrowse()],
              [sg.OK(), sg.Cancel(), sg.Button('Create new database')]]

    window = sg.Window('Find database file', layout)

    event, values = window.read()
    window.close()

    return event, values


def db_error_popup():
    sg.theme('Dark Blue')

    layout = [[sg.Text('Exiting program.')],
              [sg.Text("Database file must end in '.db'")],
              [sg.OK()]]

    window = sg.Window('Unable to find database file', layout)
    event, values = window.read()
    window.close()


def already_clocked_out_popup():
    sg.theme('Dark Blue')

    layout = [[sg.Text('You are not currently clocked in to anything.')],
              [sg.OK()]]

    window = sg.Window('Not currently clocked in', layout)

    event, values = window.read(close=True)


def get_long_text(default_long_text):
    sg.theme('Dark Blue')

    layout = [[sg.Text('There is no long text associated with the current time entry.')],
              [sg.InputText(default_text=default_long_text)],
              [sg.OK()]]

    window = sg.Window('Long text', layout)

    event, values = window.read(close=True)

    if event is None:
        return ''

    return values[0]


def format_seconds(time_in_seconds):

    hours, remainder = divmod(time_in_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return f'{hours:02}:{minutes:02}:{seconds:02}'



if __name__ == "__main__":
    # event, values = find_file()
    # print(f"event = {event}")
    # print(f"values = {values}")
    #
    # db_error_popup()

    a = get_long_text()
    print(a)
