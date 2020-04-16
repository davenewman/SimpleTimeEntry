# TODO: Include fields for clocking in to a new task
# TODO: Include clock out of current task button and display current task
# TODO: Change config file to .ini
# TODO: Read the TimeEntries table and display recent entries

import PySimpleGUI as sg
import db


class MainGUI:

    def __init__(self, db):

        self.current_clock_in = None
        self.db = db
        self.db.open()
        self.task_titles = [task[0] for task in self.db.read_task_titles()]
        print(self.task_titles)
        self.theme = sg.theme('Dark Blue')
        self.layout = [[sg.Text(f'Currently clocked in to:'), sg.Text(size=(15, 1), key='CLOCKED_IN_TO', background_color='Black')],
                       [sg.Button('Clock out of current task')],
                       [sg.Text('Task'), sg.Combo(self.task_titles, key='TASKS')],
                       [sg.Button('Clock in'), sg.Button('Exit')], ]

        self.window = sg.Window('This is template pattern 2B', self.layout)

    def run(self):

        while True:
            event, values = self.window.read()

            print(event, values)
            if event in (None, 'Exit'):
                break
            if event == 'Clock in':
                # self.window['-OUTPUT-'].update(values['-IN-'])
                self.window['CLOCKED_IN_TO'].update(self.current_clock_in)
                pass
        self.window.close()
        self.db.close()


db = db.DB()
GUI = MainGUI(db)
GUI.run()
