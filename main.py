#TODO: Check if db exists, if not create it
    #TODO: Create table TimeEntries
    #TODO: Create table Tasks
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

##sg.theme('Dark Blue 3')
##
##layout = [  [sg.Text('Filename')],
##            [sg.Input(), sg.FileBrowse()], 
##            [sg.OK(), sg.Cancel()]] 
##
##window = sg.Window('Get filename example', layout)
##
##event, values = window.Read()
##window.close()

##print(f"event = {event}\nvalues = {values}")


class DB:

    def __init__(self, db_path=config.db_info["filename"]):
        if not os.path.exists(db_path):
            event, values = utils.find_file()
            
            print(f"event = {event}\nvalues = {values}")
            print(type(event))


a = DB()

        
