import sqlite3
import utils
import os


class DB:

    def __init__(self, db_path):

        self.conn = None
        self.curs = None
        self.db_path = db_path

        if not os.path.exists(db_path): # Also verify that the tables exists.
            self._create_db()
            

    def open(self):

 
        self.conn = sqlite3.connect(self.db_path)
        self.curs = self.conn.cursor()
        self.curs.execute('''PRAGMA foreign_keys = 1''')


    def close(self):

        if self.conn:
            self.conn.commit()
            self.conn.close()
        self.conn = None
        self.curs = None

    def get_tasks(self):

        """
        Returns entire tasks table in the form of a dictionary of dictionaries
        with each key being the task name
        """

        self.curs.execute('''SELECT * from tasks''')

        query_dict = dict()
        for row in self.curs.fetchall():
            query_dict[row[0]] = {'desc': row[1], 'prep_text': row[2]}
        
        return query_dict

    def insert_time_entries(self, entries):

        self.curs.executemany('''INSERT INTO TimeEntries (date,
                                                          start_time,
                                                          end_time,
                                                          elapsed_time,
                                                          task,
                                                          long_text) 
                                    VALUES (?, ?, ?, ?, ?, ?)''', entries)
        self.conn.commit()

    def insert_tasks(self, package):

        self.curs.executemany('''INSERT INTO tasks (title,
                                                        desc,
                                                        prep_text)
                                        VALUES (?, ?, ?)''', package)
        self.conn.commit()


    def get_entries(self):
        '''
        Returns entire timeentries table in the form of a dictionary of dictionaries
        with each key being the id number.
        '''

        self.curs.execute('''SELECT * from timeentries''')

        query_dict = dict()
        for row in self.curs.fetchall():
            query_dict[row[0]] = {'date': row[1], 'start_time': row[2],
                                  'end_time': row[3], 'elapsed_time': row[4],
                                  'task': row[5], 'long_text': row[6]}

        return query_dict


    def update_entries(self, package):

        """

        Update an entry in the timeentries table
        
        """

        self.curs.executemany('''UPDATE timeentries
                                SET date = ?,
                                    start_time = ?,
                                    end_time = ?,
                                    elapsed_time = ?,
                                    task = ?,
                                    long_text = ?
                                WHERE id = ?''', package)

        self.conn.commit()



                                                    #title, desc, prep_text

    def update_tasks(self, package):
        """
        Update an entry in the tasks table
        """

        self.curs.executemany('''UPDATE tasks
                                SET title = ?,
                                    desc = ?,
                                    prep_text = ?
                                WHERE title = ?''', package)


        self.conn.commit()



    def delete_entry(self, entry_id):
        """

        Delete an entry in the timeentries table
    
        """

        self.curs.execute('''DELETE FROM timeentries WHERE id=?''', (entry_id,))

        self.conn.commit()

        


    def _create_db(self):

        self.open()

        self.curs.execute('''CREATE TABLE TimeEntries (
                            id INTEGER PRIMARY KEY,
                            date TEXT,
                            start_time TEXT,
                            end_time TEXT,
                            elapsed_time REAL,
                            task TEXT,
                            long_text TEXT,
                            FOREIGN KEY (task) REFERENCES Tasks (title)
                            ON UPDATE CASCADE ON DELETE CASCADE)''')

        self.curs.execute('''CREATE TABLE Tasks (
                                    title TEXT PRIMARY KEY,
                                    desc TEXT,
                                    prep_text TEXT)''')

        # Insert a single default task into the tasks table

        self.insert_tasks([('Uncategorized', 'Uncategorized tasks', 'Uncategorized - ')])

        self.conn.commit()

        self.close()



if __name__ == "__main__":

    import random
    import datetime

    if os.path.exists('test.db'):
        os.remove('test.db')
    
    database = DB('test.db')

    def random_data():

        date = f"{random.randint(1,30):02}/{random.randint(1,12):02}/2020"
        time = f"{random.randint(0, 24):02}:{random.randint(0, 60):02}:{random.randint(0, 60):02}"
        elapsed_time = f"{10 * random.random():.3f}"
        task = random.choice(['Uncategorized', 'Overhead', 'Billed'])
        package = []

        return date, time, elapsed_time, task
    
