# TODO: Change config file to .ini
# TODO: Fix newline bug in long text

import PySimpleGUI as sg
from TimeHandler import TimeHandler, AlreadyClockedOutError, LongTextNotUpdatedError, TaskDoesNotExistError
from db import DB
import config
import datetime
import utils
import os
from sqlite3 import IntegrityError

def mainGUI(settings, t_e):

    theme = sg.theme('Dark Blue')

    t_e.db.open()
    tasks = t_e.db.get_tasks()
    task_list = sorted(tasks.keys(), key=str.lower)
    table_entries = format_entries(t_e.db.get_entries())
    table_tasks = format_tasks(t_e.db.get_tasks())

    menu_layout = [['File', ['Output to CSV','Settings','Tasks','Exit']],
                        ['Help', ['Documentation']]]

# -------------------------  Tab 1 layout  ------------------------- #

    top_frame_layout = [[sg.Text('Currently clocked in to:'),
                            sg.Text(size=(15, 1), key='-CLOCKED_IN_TO-', background_color='black', text_color='white', enable_events=True),
                            sg.Text('for'), sg.Text('00:00:00',size=(10, 1), key='-TIME_CLOCKED_IN-')],
                            [sg.Button('Clock out of current task', size=(35,3)), sg.Button('Edit long text for current task', size=(35,3))],]

    bottom_frame_layout = [[sg.Text('Task'),
                                sg.InputOptionMenu(task_list, key='-TASKS-', default_value=task_list[0])],
                               [sg.Button('Clock in', size=(72,4))], ]

    tab_one_layout = [[sg.Frame('',top_frame_layout)],[sg.Frame('',bottom_frame_layout)]]

# -------------------------  Tab 2 layout  ------------------------- #

    headings_1 = ['Date','Start','End','Elapsed', 'Task','Description']

    editor_top = [[sg.Table(values=table_entries,
                headings=headings_1,
                auto_size_columns=False,
                col_widths=[8, 7, 7, 7, 12, 22],
                justification='left',
                num_rows=9,
                key='-TABLE_1-')]]
    
    editor_bottom = [[sg.Button('Update/View Entry', size=(23,1)), sg.Button('Delete Entry', size=(22,1)), sg.Button('Add Entry', size=(23,1))]]

    tab_two_layout = [[sg.Frame('', editor_top)], [sg.Frame('', editor_bottom)]]

# -------------------------  Tab 3 layout  ------------------------- #

    headings_2 = ['Title', 'Description', 'Default Text']

    task_top = [[sg.Table(values=table_tasks,
                headings=headings_2,
                auto_size_columns=False,
                col_widths=[13, 32, 18],
                justification='left',
                num_rows=9,
                key='-TABLE_2-')]]

    task_bottom = [[sg.Button('Update/View Task', size=(35,1)), sg.Button('Add Task', size=(35,1))]]

    tab_three_layout = [[sg.Frame('', task_top)], [sg.Frame('', task_bottom)]]

    
    
    
    
    
    layout = [[sg.Menu(menu_layout),
                sg.TabGroup([[sg.Tab('Clock In/Clock Out', tab_one_layout)],
                             [sg.Tab('Editor', tab_two_layout)],
                             [sg.Tab('Tasks', tab_three_layout)] ])]]
    
    window = sg.Window('Simple Time Entry', layout)


    while True:
        event, values = window.read(timeout=1000)
        
        if t_e.clocked_in:
            t_e.calculate_time_clocked_in()
            time_formatted = utils.format_seconds(t_e.calculate_time_clocked_in())
            window['-TIME_CLOCKED_IN-'].update(time_formatted)

        if event in (None, 'Exit'):
            if t_e.clocked_in:
                try:
                    t_e.clock_out()
                    
                except LongTextNotUpdatedError:
                    _event, _values = utils.get_long_text(t_e.long_text)
                    if _event == 'OK':
                        t_e.update_long_text(_values['-TEXT-'])
                        t_e.clock_out()
                    else:
                        continue

            db.close()
            break

        if event == 'Clock in':

            window['-TIME_CLOCKED_IN-'].update('00:00:00')
            window['-CLOCKED_IN_TO-'].update('')

            if t_e.clocked_in:

                try:
                    t_e.clock_out()
                    table_entries = format_entries(t_e.db.get_entries())
                    window['-TABLE_1-'].update(table_entries)
                    
                except LongTextNotUpdatedError:
                    _event, _values = utils.get_long_text(t_e.long_text)
                    if _event == 'OK':
                        t_e.update_long_text(_values['-TEXT-'])
                        t_e.clock_out()
                        table_entries = format_entries(t_e.db.get_entries())
                        window['-TABLE_1-'].update(table_entries)
                    else:
                        continue
                    

            t_e.clock_in(values['-TASKS-'], tasks[values['-TASKS-']]['prep_text'])
            window['-CLOCKED_IN_TO-'].update(t_e.current_task)

        if event == 'Clock out of current task':
            window['-TIME_CLOCKED_IN-'].update('00:00:00')
            window['-CLOCKED_IN_TO-'].update('')

            try:
                t_e.clock_out()

            except AlreadyClockedOutError:
                utils.already_clocked_out_popup()

            except LongTextNotUpdatedError:
                _event, _values = utils.get_long_text(t_e.long_text)
                if _event == 'OK':
                    t_e.update_long_text(_values['-TEXT-'])
                    t_e.clock_out()

            table_entries = format_entries(t_e.db.get_entries())
            window['-TABLE_1-'].update(table_entries)
            
        if event == 'Edit long text for current task':

            if t_e.clocked_in:
                _event, _values = utils.get_long_text(t_e.long_text)
                t_e.update_long_text(_values['-TEXT-'])
                
            else:
                utils.already_clocked_out_popup()

                
        if event == 'Update/View Entry' and values['-TABLE_1-'] and table_entries:               
            
            # ind contains the row number in the table
            ind = values['-TABLE_1-'][0]
            row = table_entries[ind]

            _event, _values = entry_details(task_list, package=row)
            
            if _event == 'Submit':

                t_e.db.update_entries([(_values['-DATE-'],
                                        _values['-S_TIME-'],
                                        _values['-E_TIME-'],
                                        _values['-ELAPSE-'],
                                        _values['-TASK-'],
                                        _values['-DTEXT-'],
                                        row[-1])])
                
                table_entries = format_entries(t_e.db.get_entries())
                window['-TABLE_1-'].update(table_entries)


        if event == 'Add Entry':

            _event, _values = entry_details(task_list)
            
            if _event == 'Submit':

                t_e.db.insert_time_entries([(_values['-DATE-'],
                                             _values['-S_TIME-'],
                                             _values['-E_TIME-'],
                                             _values['-ELAPSE-'],
                                             _values['-TASK-'],
                                             _values['-DTEXT-'])])

                table_entries = format_entries(t_e.db.get_entries())
                window['-TABLE_1-'].update(table_entries)

        if event == 'Delete Entry' and values['-TABLE_1-'] and table_entries:

            ind = values['-TABLE_1-'][0]
            entry_id = table_entries[ind][-1]
            t_e.db.delete_entry(entry_id)
            table_entries = format_entries(t_e.db.get_entries())
            window['-TABLE_1-'].update(table_entries)


        if event == 'Update/View Task' and values['-TABLE_2-']:
            
            ind = values['-TABLE_2-'][0]
            row = table_tasks[ind]

            # Prevent user from updating current task
            if row[0] == t_e.current_task:
                utils.cant_update_current_task_popup()
                continue
            _event, _values = task_details(package=row)

            if _event == 'Submit':

                try:
                    t_e.db.update_tasks([(_values['-TITLE-'],
                                          _values['-DESC-'],
                                          _values['-PTEXT-'],
                                          row[0])])

                except IntegrityError:
                    utils.need_unique_task_popup()

                tasks = t_e.db.get_tasks()
                task_list = sorted(tasks.keys(), key=str.lower)
                table_entries = format_entries(t_e.db.get_entries())
                table_tasks = format_tasks(tasks)
                window['-TABLE_2-'].update(table_tasks)
                window['-TABLE_1-'].update(table_entries)
                window['-TASKS-'].update(values=task_list)

        if event == "Add Task":

            _event, _values = task_details()

            if _event == 'Submit':

                try:
                    t_e.db.insert_tasks([(_values['-TITLE-'],
                                          _values['-DESC-'],
                                          _values['-PTEXT-'])])

                except IntegrityError:
                    utils.need_unique_task_popup()

                tasks = t_e.db.get_tasks()
                task_list = sorted(tasks.keys(), key=str.lower)
                table_entries = format_entries(t_e.db.get_entries())
                table_tasks = format_tasks(tasks)
                window['-TABLE_2-'].update(table_tasks)
                window['-TABLE_1-'].update(table_entries)
                window['-TASKS-'].update(values=task_list)
                
            

    window.close()


def format_entries(nested_dict):
    """Format time entries for table on tab two"""
    return [[val['date'], val['start_time'],
             val['end_time'], val['elapsed_time'],
             val['task'], val['long_text'], key]
            for key, val in nested_dict.items()]

def format_tasks(nested_dict):
    """Format tasks for table on tab three"""
    return [[key, val['desc'], val['prep_text']]
            for key, val in nested_dict.items()]

def entry_details(task_list, package=['','','','','','']):
    """
    This method provides a singular place to contain the entry details layout
    since it is used both to update entries as well as add new entries.
    """
    layout = [[sg.Text('Task', size=(15,1)), sg.InputOptionMenu(task_list, key='-TASK-', default_value=package[4])],
              [sg.Text('Date', size=(15,1)), sg.InputText(default_text=package[0], key='-DATE-')],
              [sg.Text('Start Time', size=(15,1)), sg.InputText(default_text=package[1], key='-S_TIME-')],
              [sg.Text('End Time', size=(15,1)), sg.InputText(default_text=package[2], key='-E_TIME-')],
              [sg.Text('Elapsed Time', size=(15,1)), sg.InputText(default_text=package[3], key='-ELAPSE-')],
              [sg.Text('Description', size=(15,1)), sg.Multiline(default_text=package[5], key='-DTEXT-')],
              [sg.Button('Submit'), sg.Button('Cancel')]]

    window = sg.Window('Details View', layout)

    event, values = window.read(close=True)

    return event, values


def task_details(package=['','','']):
    """
    This method provides a singular place to contain the task details layout
    since it is used both to update tasks as well as add new tasks.
    """

    layout = [[sg.Text('Task Title', size=(15,1)), sg.InputText(default_text=package[0], key='-TITLE-', )],
              [sg.Text('Description', size=(15,1)), sg.Multiline(default_text=package[1], key='-DESC-')],
              [sg.Text('Default Text', size=(15,1)), sg.InputText(default_text=package[2], key='-PTEXT-')],
              [sg.Button('Submit'), sg.Button('Cancel')]]

    window = sg.Window('Details View', layout)

    event, values = window.read(close=True)

    return event, values




if __name__ == "__main__":

    # If the config file exists...

    db_path = config.db_info['filename'] 
    if not os.path.exists(db_path):
        event, values = utils.find_file()
        if event.lower() == 'ok' and values[0].endswith('db'):
            db_path = values[0]
        elif event.lower() == 'create new database':
            db_path = 'TimeEntry.db'
        else:
            utils.db_error_popup()
            exit()

    db = DB(db_path)
    timehandler = TimeHandler(db)
    settings = None
    mainGUI(settings, timehandler)
