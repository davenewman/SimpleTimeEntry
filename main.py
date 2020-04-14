
# TODO: Read the TimeEntries table and display recent entries
# make sure to handle the case in which there are no entries to the table
# can the entries be editable?
# TODO: Include fields for clocking in to a new task
# TODO: Include clock out of current task button and display current task
# TODO: Config file?
# DB name

# import PySimpleGUI as sg
import sqlite3
import config
import utils
import os


class DB:

    def __init__(self, db_path=config.db_info['filename']):

        self.conn = None
        self.cursor = None

        if os.path.exists(db_path):
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

    def close(self):

        self.conn.commit()
        self.conn.close()

    def read_task_titles(self):

        self.cursor.execute('''SELECT task_title from Tasks''')
        return self.cursor.fetchall()

    def _t_insert_time_entries(self, entries):

        self.cursor.executemany('''INSERT INTO TimeEntries (task_id, start_time, end_time, elapsed_time, long_text) 
                                    VALUES (?, ?, ?, ?, ?)''', entries)

        self.close()

    def create_db(self):

        self.open()

        try:
            self.cursor.execute('''CREATE TABLE TimeEntries (
                                    id integer PRIMARY KEY,
                                    task_id integer NOT NULL,
                                    start_time text,
                                    end_time text,
                                    elapsed_time real NOT NULL,
                                    long_text text,
                                    FOREIGN KEY (task_ID) REFERENCES Tasks (id))''')
        except sqlite3.Error as e:
            print(e)
            self.close()

        try:
            self.cursor.execute('''CREATE TABLE Tasks (
                                    id integer PRIMARY KEY,
                                    task_title text NOT NULL,
                                    task_description text NOT NULL)''')
        except sqlite3.Error as e:
            print(e)
            self.close()

        try:
            self.cursor.executemany('''INSERT INTO Tasks (task_title, task_description) VALUES (?, ?)''',
                                    config.db_info['tasks'])

        except sqlite3.Error as e:
            print(e)
            self.close()

        self.close()


if __name__ == "__main__":

    import random
    import datetime

    def put_entry_in_table():
        db_obj = DB()
        task_ids = [1, 2, 3, 4, 5]
        now = datetime.datetime.now()
        later = datetime.datetime.now() + datetime.timedelta(hours=10*random.random())
        words = ['lorem','ipsum','words','dolor','sit','amet']
        mydata = [(random.choice(task_ids), now.strftime('%d-%m-%Y %H:%M:%S'),
                   later.strftime('%d-%m-%Y %H:%M:%S'), (later - now).seconds / 3600 ,random.choice(words))]
        db_obj._t_insert_time_entries(mydata)


    for num in range(100):
        put_entry_in_table()



