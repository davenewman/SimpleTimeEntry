import os

db_info = {
    'filename': os.path.join(os.getcwd(), 'simpletimeentry-2.db'),
    'tasks': [('Administration', 'Tasks such as email, preparing for sessions, completing documents, and other duties as assigned', 'Administration - '),
              ('Trainings', 'Compliance, mandatory, and/or pre-approved or assigned by manager', 'Trainings - '),
              ('Mentoring', 'Assisting a teammate with Microsoft Teams practice/questions', 'Mentoring - '),
              ('Coaching sessions', 'Manager/Director led', 'Coaching sessions - '),
              ('More tasks', 'This is the task description', 'More tasks - '),]
}
