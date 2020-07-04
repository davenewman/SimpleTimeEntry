# TODO: Change config file to .ini
# TODO: Read the TimeEntries table and display recent entries (in a new tab?)

import PySimpleGUI as sg
import db
import datetime
import utils


class MainGUI:

    def __init__(self, db):

        # This instance of TimeEntries is just to read the database for the task list and later to read the most recent
        # time entries most likely
        self.t_e = TimeEntries(db)

        theme = sg.theme('Dark Blue')

        # The menu layout will be global to both tabs

        self.menu_layout = [['File', ['Settings','Output to CSV','Exit']],
                            ['Help', ['Documentation']]]

        self.top_frame_layout = [[sg.Text('Currently clocked in to:'),
                                sg.Text(size=(15, 1), key='-CLOCKED_IN_TO-', background_color='black', text_color='white', enable_events=True),
                                sg.Text('for'), sg.Text('00:00:00',size=(10, 1), key='-TIME_CLOCKED_IN-')],
                                [sg.Button('Clock out of current task', size=(35,4)), sg.Button('Edit long text for current task', size=(35,4))],]

        self.bottom_frame_layout = [[sg.Text('Task'),
                                    sg.InputOptionMenu(self.t_e.task_list, key='-TASKS-', default_value=self.t_e.task_list[0])],
                                   [sg.Button('Clock in', size=(72,5), pad=(5,30))], ]


        # The editor layout will have to be populated with all of the contents from the timeentries database...
        #[[row1],[row2]]
        
##        self.editor_top = [[sg.Text('Date'), sg.Text('Start Time'), sg.Text('End Time'), sg.Text('Elapsed Time'), sg.Text('This is a lot of descriptive text I do not think it will fit on the screen', size=(18,1))],
##                           [sg.Text('Date'), sg.Text('Start Time'), sg.Text('End Time'), sg.Text('Elapsed Time'), sg.Text('This is a lot of descriptive text I do not think it will fit on the screen', size=(1,1))],
##                           [sg.Text('Date'), sg.Text('Start Time'), sg.Text('End Time'), sg.Text('Elapsed Time'), sg.Text('This is a lot of descriptive text I do not think it will fit on the screen', size=(1,1))],
##                           [sg.Text('Date'), sg.Text('Start Time'), sg.Text('End Time'), sg.Text('Elapsed Time'), sg.Text('This is a lot of descriptive text I do not think it will fit on the screen', size=(1,1))],
##                           [sg.Text('Date'), sg.Text('Start Time'), sg.Text('End Time'), sg.Text('Elapsed Time'), sg.Text('This is a lot of descriptive text I do not think it will fit on the screen', size=(1,1))],
##                           [sg.Text('Date'), sg.Text('Start Time'), sg.Text('End Time'), sg.Text('Elapsed Time'), sg.Text('This is a lot of descriptive text I do not think it will fit on the screen', size=(1,1))],
##                           [sg.Text('Date'), sg.Text('Start Time'), sg.Text('End Time'), sg.Text('Elapsed Time'), sg.Text('This is a lot of descriptive text I do not think it will fit on the screen', size=(1,1))],
##                           [sg.Text('Date'), sg.Text('Start Time'), sg.Text('End Time'), sg.Text('Elapsed Time'), sg.Text('This is a lot of descriptive text I do not think it will fit on the screen', size=(1,1))],
##                           [sg.Text('Date'), sg.Text('Start Time'), sg.Text('End Time'), sg.Text('Elapsed Time'), sg.Text('This is a lot of descriptive text I do not think it will fit on the screen', size=(1,1))],
##                           [sg.Text('Date'), sg.Text('Start Time'), sg.Text('End Time'), sg.Text('Elapsed Time'), sg.Text('This is a lot of descriptive text I do not think it will fit on the screen', size=(1,1))],
##                           [sg.Text('Date'), sg.Text('Start Time'), sg.Text('End Time'), sg.Text('Elapsed Time'), sg.Text('This is a lot of descriptive text I do not think it will fit on the screen', size=(1,1))],
##                           [sg.Text('Date'), sg.Text('Start Time'), sg.Text('End Time'), sg.Text('Elapsed Time'), sg.Text('This is a lot of descriptive text I do not think it will fit on the screen', size=(1,1))],
##                           [sg.Text('Date'), sg.Text('Start Time'), sg.Text('End Time'), sg.Text('Elapsed Time'), sg.Text('This is a lot of descriptive text I do not think it will fit on the screen', size=(1,1))],
##                           [sg.Text('Date'), sg.Text('Start Time'), sg.Text('End Time'), sg.Text('Elapsed Time'), sg.Text('This is a lot of descriptive text I do not think it will fit on the screen', size=(1,1))]]

        now = datetime.datetime.now()
        now_date = now.strftime('%d-%m-%Y')
        now_time = now.strftime('%H:%M:%S')

        date_col = [[sg.Text('Date')], [sg.Text(now_date)],[sg.Text(now_date)],[sg.Text(now_date)],[sg.Text(now_date)],[sg.Text(now_date)],[sg.Text(now_date)],[sg.Text(now_date)],[sg.Text(now_date)],[sg.Text(now_date)],[sg.Text(now_date)], ]
        
        start_time_col = [[sg.Text('Start')], [sg.Text(now_time)],[sg.Text(now_time)],[sg.Text(now_time)],[sg.Text(now_time)],[sg.Text(now_time)],[sg.Text(now_time)],[sg.Text(now_time)],[sg.Text(now_time)],[sg.Text(now_time)],[sg.Text(now_time)],]
        
        end_time_col = [[sg.Text('End')], [sg.Text(now_time)], [sg.Text(now_time)], [sg.Text(now_time)], [sg.Text(now_time)], [sg.Text(now_time)], [sg.Text(now_time)], [sg.Text(now_time)], [sg.Text(now_time)], [sg.Text(now_time)], [sg.Text(now_time)]]
        
        elapsed_time_col = [[sg.Text('Elapsed')], [sg.Text('10.005')],[sg.Text('10.005')],[sg.Text('10.005')],[sg.Text('10.005')],[sg.Text('10.005')],[sg.Text('10.005')],[sg.Text('10.005')],[sg.Text('10.005')],[sg.Text('10.005')],[sg.Text('10.005')]]
        
        desc_text_col = [[sg.Text('Descriptive Text')], [sg.Text('This is some very, very, very long long text that you can not possibly all print.')],[sg.Text('This is some very, very, very long long text that you can not possibly all print.')],[sg.Text('This is some very, very, very long long text that you can not possibly all print.')],[sg.Text('This is some very, very, very long long text that you can not possibly all print.')],[sg.Text('This is some very, very, very long long text that you can not possibly all print.')],[sg.Text('This is some very, very, very long long text that you can not possibly all print.')],[sg.Text('This is some very, very, very long long text that you can not possibly all print.')],[sg.Text('This is some very, very, very long long text that you can not possibly all print.')], ]

        edit_col = [[sg.Button('Edit/View')] for num in range(10)]
        
        self.editor_top = [[sg.Column(date_col), sg.Column(start_time_col), sg.Column(end_time_col), sg.Column(elapsed_time_col), sg.Column(desc_text_col, size=(200,200)), sg.Column(edit_col)]]
        self.editor_bottom = [[sg.Button('Previous Entries', size=(35,1)), sg.Button('Next Entries', size=(35,1))]]
        
        self.tab_one_layout = [[sg.Frame('',self.top_frame_layout, pad=(5,10))],[sg.Frame('',self.bottom_frame_layout, pad=(5,10))]]
        self.tab_two_layout = [[sg.Frame('', self.editor_top)], [sg.Frame('', self.editor_bottom)]]
        
        self.layout = [[sg.Menu(self.menu_layout), sg.TabGroup([[sg.Tab('Clock In/Clock Out', self.tab_one_layout)], [sg.Tab('Editor', self.tab_two_layout)]])]]
        self.window = sg.Window('Simple Time Entry', self.layout)

    def run(self):

        while True:
            event, values = self.window.read(timeout=1000)
            print(event)
            print(values)
            if self.t_e.clocked_in:
                self.t_e.calculate_time_clocked_in()
                time_formatted = utils.format_seconds(self.t_e.current_clock_in_time)
                self.window['-TIME_CLOCKED_IN-'].update(time_formatted)
                #print(f"Clocked in to {self.t_e.current_task} for {self.t_e.current_clock_in_time} seconds")

            if event in (None, 'Exit'):
                if self.t_e.clocked_in:
                    self.t_e.clock_out()
                break

            if event == 'Clock in':

                self.reset_window()

                if self.t_e.clocked_in:
                    self.t_e.clock_out()

                # This is the first effective time entry
                self.t_e = TimeEntries(db)
                self.t_e.clock_in(values['-TASKS-'])
                self.window['-CLOCKED_IN_TO-'].update(self.t_e.current_task)


            if event == 'Clock out of current task':
                # clock out and reset the class!
                self.reset_window()
                self.t_e.clock_out()
                

                # reset the class by creating a new instance
                self.t_e = TimeEntries(db)

                
            if event == 'Edit long text for current task':

                if self.t_e.clocked_in:
                    self.t_e.long_text = utils.get_long_text(self.t_e.long_text)
                    self.t_e.long_text_updated = True
                else:
                    utils.already_clocked_out_popup()

            

        self.window.close()

    def reset_window(self):
        self.window['-TIME_CLOCKED_IN-'].update('00:00:00')
        self.window['-CLOCKED_IN_TO-'].update('')


        


class TimeEntries:
    """
    The TimeEntries class contains all database connections and methods relating to the backend of the application.
    """

    def __init__(self, database):

        self.database = database

        self.database.open()
        self.task_list = self.database.read_task_titles()
        self.task_descriptions = self.database.read_task_descriptions()
        self.long_text_prepend = self.database.read_task_desc_text()

        self.clocked_in = False
        self.start_time = None
        self.end_time = None
        self.current_clock_in_time = None
        self.current_task = None
        self.long_text_updated = False
        self.long_text = '' # Needs to be populated from the tasks table

    def clock_in(self, task):

        if self.clocked_in:
            self.clock_out()

        else:
            self.current_task = task
            self.long_text = self.long_text_prepend[self.task_list.index(self.current_task)]
            self.clocked_in = True
            self.start_time = datetime.datetime.now()

    def clock_out(self):

        """ Clock out of current task. """

        if self.clocked_in:
            self.end_time = datetime.datetime.now()
            self.db_insert()

        else:
            utils.already_clocked_out_popup()

    def calculate_time_clocked_in(self):
        """ Populate current_clock_in_time with time elapsed in seconds. """

        time_diff = datetime.datetime.now() - self.start_time
        #self.current_clock_in_time = round(float(time_diff.seconds) / 3600, 3)
        self.current_clock_in_time = time_diff.seconds

        
    def db_insert(self):

        if not self.long_text_updated:
            self.long_text = utils.get_long_text(self.long_text)

        # [task_id, start_date, start_time, end_date, end_time, elapsed_time, long_text]

        start_date = self.start_time.strftime('%d-%m-%Y')
        start_time = self.start_time.strftime('%H:%M:%S')
        end_date = self.end_time.strftime('%d-%m-%Y')
        end_time = self.end_time.strftime('%H:%M:%S')
        elapsed_time = round( float(self.current_clock_in_time) / 3600, 3)

        package = [(self.task_list.index(self.current_task) + 1, start_date, start_time,
                    end_date, end_time, elapsed_time, self.long_text)]

        for item in package:
            print(f"{item}: {type(item)}")

        self.database.insert_time_entries(package)
        self.database.close()

if __name__ == "__main__":
    db = db.DB()
    GUI = MainGUI(db)
    GUI.run()
