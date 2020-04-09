#TODO: Read the TimeEntries table and display recent entries
    # make sure to handle the case in which there are no entries to the table
    # can the entries be editable?
#TODO: Include fields for clocking in to a new task
#TODO: Include clock out of current task button and display current task
#TODO: Config file?
    # DB name
    
import PySimpleGUI as sg
import sqlite3
import config
import utils
import os

class DB:

    def __init__(self, db_path=config.db_info['filename']):
        
        if  os.path.exists(db_path):
            self.db_path = db_path

        else:
            event, values = utils.find_file()
            if event.lower() == 'ok' and values[0].endswith('db'):
                self.db_path = values[0]
            elif event.lower() == 'create new database':
                self.db_path = db_path
                self.create_db()
            else:
                utils.db_error_popup()
                exit()
        self.open()

    def open(self):

        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()

        except sqlite3.Error as e:
            print("Error")

    def create_db(self):

        self.open()

        try:
            self.cursor.execute('''CREATE TABLE TimeEntries (
                                    id integer PRIMARY KEY,
                                    task_id integer,
                                    date text NOT NULL,
                                    start_time text NOT NULL,
                                    end_time text NOT NULL,
                                    elapsed_time text NOT NULL,
                                    FOREIGN KEY (task_ID) REFERENCES Tasks (id))''')
        except sqlite3.Error as e:
            print(e)

        try:
            self.cursor.execute('''CREATE TABLE Tasks (
                                    id integer PRIMARY KEY,
                                    task_title text NOT NULL,
                                    task_description text NOT NULL)''')
        except sqlite3.Error as e:
            print(e)
        


a = DB()

        
