import PySimpleGUI as sg
import os
import configparser



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

def need_unique_task_popup():

    layout = [[sg.Text('That task name already exists. The task name must be unique.')],
              [sg.OK()]]

    window = sg.Window('Task name already exists', layout)

    event, values = window.read(close=True)

def cant_update_current_task_popup():

    layout = [[sg.Text('You are currently clocked into this task.\nPlease clock out before making changes.')],
              [sg.OK()]]

    window = sg.Window('Task name already exists', layout)

    event, values = window.read(close=True)

def get_long_text(default_long_text):
    sg.theme('Dark Blue')

    layout = [[sg.Text('Enter long text below.')],
              [sg.Multiline(default_text=default_long_text, key='-TEXT-')],
              [sg.OK()]]

    window = sg.Window('Long text', layout)

    event, values = window.read(close=True)

    return event, values


def format_seconds(time_in_seconds):

    hours, remainder = divmod(time_in_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return f'{hours:02}:{minutes:02}:{seconds:02}'



def settings():

    return None



if __name__ == "__main__":

    a = get_long_text("Default text")
    print(a)
