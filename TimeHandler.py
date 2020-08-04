import datetime
import utils

class TimeHandler:

    def __init__(self, db, require_long_text=True):

        self.db = db
        self.clocked_in = False
        self.start_time = None
        self.end_time = None
        self.current_task = None
        self.require_long_text = require_long_text
        self.long_text_updated = False
        self.long_text = None

    def clock_in(self, task_name, prep_text):

        if self.clocked_in:
            self.clock_out()

        else:
            # Raise the exception now to avoid collecting time data for a task
            # that does not exist and trying to insert into the database which
            # will result in an IntegrityError
            if task_name not in list(self.db.get_tasks().keys()):
                raise TaskDoesNotExistError
            else:
                self.current_task = task_name            
                self.long_text = prep_text
                self.clocked_in = True
                self.start_time = datetime.datetime.now()

    def clock_out(self):

        """ Clock out of current task. """

        if self.clocked_in:
            self.end_time = datetime.datetime.now()
            self._db_insert()

            # Reset the attributes 
            self.clocked_in = False
            self.start_time = None
            self.end_time = None
            self.current_clock_in_time = None
            self.current_task = None
            self.long_text_updated = False
            self.long_text = None
            
        else:
            raise AlreadyClockedOutError

    def calculate_time_clocked_in(self):
        """Populate current_clock_in_time with time elapsed in seconds. """

        time_diff = datetime.datetime.now() - self.start_time
        return time_diff.seconds

    def update_long_text(self, text):
        """Method to update long text as well as change the bool to true"""
        self.long_text = text
        self.long_text_updated = True

        
    def _db_insert(self):

        """ 
        This method is meant to insert entries
        into the database "organically" - if the application has been tracking
        its own time. Entries may also be inserted by calling the
        insert_time_entries method of the database class directly.
        """

        if (not self.long_text_updated) and self.require_long_text:
            raise LongTextNotUpdatedError

        # [task_id, start_date, start_time, end_date, end_time, elapsed_time, long_text]

        date = self.start_time.strftime('%d-%m-%Y')
        start_time = self.start_time.strftime('%H:%M')
        end_time = self.end_time.strftime('%H:%M')
        elapsed_time = round( float(self.calculate_time_clocked_in()) / 3600, 3)

        package = [(date, start_time, end_time,
                    elapsed_time, self.current_task, self.long_text)]

        self.db.open()
        self.db.insert_time_entries(package)

class AlreadyClockedOutError(Exception):
    pass

class LongTextNotUpdatedError(Exception):
    pass

class TaskDoesNotExistError(Exception):
    pass

if __name__ == "__main__":

    import db
    db = db.DB('dummy.db')
    db.open()
    tasks_dict = db.get_tasks()
    task = list(tasks_dict.keys())[0]
    task_details = tasks_dict[task]['prep_text']
    timehandler = TimeHandler(db, require_long_text=False)
    timehandler.clock_in(task, task_details)
    timehandler.clock_out()
    timehandler.clock_out()
    

