# TODO: Include fields for clocking in to a new task
# TODO: Include clock out of current task button and display current task
# TODO: Change config file to .ini
# TODO: Read the TimeEntries table and display recent entries

import PySimpleGUI as sg
import db
import datetime
import utils


class MainGUI:

    def __init__(self, db):

        # This instance of TimeEntries is just to read the database for the task list and later to read the most recent
        # time entries most likely
        self.t_e = TimeEntries(db)

        self.theme = sg.theme('Dark Blue')
        self.layout = [[sg.Text('Currently clocked in to:'),
                        sg.Text(size=(15, 1), key='-CLOCKED_IN_TO-', background_color='Black', enable_events=True),
                        sg.Text('for'), sg.Text(size=(10, 1), key='-TIME_CLOCKED_IN-')],
                       [sg.Button('Clock out of current task'), sg.Button('Edit long text for current task')],
                       [sg.Text('Task'),
                        sg.Combo(self.t_e.task_list, key='-TASKS-', default_value=self.t_e.task_list[0])],
                       [sg.Button('Clock in'), sg.Button('Exit')], ]

        self.window = sg.Window('This is template pattern 2B', self.layout)

    def run(self):

        while True:
            event, values = self.window.read(timeout=1000)
            print(f'self.clocked_in = {self.t_e.clocked_in}')
            print(f'long text = {self.t_e.long_text}')
            print(f'event = {event}\n\n')
            self.window['-CLOCKED_IN_TO-'].update(self.t_e.current_task)
            if self.t_e.clocked_in:
                self.t_e.calculate_time_clocked_in()
                time_formatted = utils.format_seconds(self.t_e.current_clock_in_time)
                self.window['-TIME_CLOCKED_IN-'].update(time_formatted)
                print(f"Clocked in to {self.t_e.current_task} for {self.t_e.current_clock_in_time} seconds")

            else:
                self.window['-TIME_CLOCKED_IN-'].update('N/A')

            if event in (None, 'Exit'):
                if self.t_e.clocked_in:
                    self.t_e.clock_out()
                break

            if event == 'Clock in':

                if self.t_e.clocked_in:
                    self.t_e.clock_out()

                # This is the first effective time entry
                self.t_e = TimeEntries(db)
                self.t_e.clock_in(values['-TASKS-'])


            if event == 'Clock out of current task':
                # clock out and reset the class!
                self.t_e.clock_out()

                # reset the class by creating a new instance
                self.t_e = TimeEntries(db)

            if event == 'Edit long text for current task':

                if self.t_e.clocked_in:
                    self.t_e.long_text = utils.get_long_text(self.t_e.long_text)
                else:
                    utils.already_clocked_out_popup()

        self.window.close()


class TimeEntries:
    """
    The TimeEntries class contains all database connections and methods relating to the backend of the application.
    """

    def __init__(self, database):

        self.database = database

        self.database.open()
        self.task_list = self.database.read_task_titles()
        self.task_descriptions = self.database.read_task_descriptions()

        self.clocked_in = False
        self.start_time = None
        self.end_time = None
        self.current_clock_in_time = None
        self.current_task = None
        self.long_text = ''

    def clock_in(self, task):

        if self.clocked_in:
            self.clock_out()

        else:
            self.current_task = task
            self.clocked_in = True
            self.start_time = datetime.datetime.now()

    def clock_out(self):

        if self.clocked_in:
            self.end_time = datetime.datetime.now()
            self.db_insert()

        else:
            utils.already_clocked_out_popup()

    def calculate_time_clocked_in(self):

        self.current_clock_in_time = (datetime.datetime.now() - self.start_time).seconds

    def db_insert(self):

        if not self.long_text:
            self.long_text = utils.get_long_text(self.long_text)

        # [task_id, start_time, end_time, elapsed_time, long_text]
        start = self.start_time.strftime('%d-%m-%Y %H:%M:%S')
        end = self.end_time.strftime('%d-%m-%Y %H:%M:%S')

        package = [(self.task_list.index(self.current_task) + 1, start, end, self.current_clock_in_time,
                   self.long_text)]

        for item in package:
            print(f"{item}: {type(item)}")

        self.database.insert_time_entries(package)
        self.database.close()


if __name__ == "__main__":
    db = db.DB()
    GUI = MainGUI(db)
    GUI.run()
