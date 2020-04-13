import os

db_info = {
    'filename': os.path.join(os.getcwd(), 'simpletimeentry.db'),
    'tasks': [('Administration', 'Tasks such as email, preparing for sessions, completing documents, and other duties as assigned'),
              ('Trainings', 'Compliance, mandatory, and/or pre-approved or assigned by manager'),
              ('Mentoring', 'Assisting a teammate with Microsoft Teams practice/questions'),
              ('Coaching sessions', 'Manager/Director led')]
}
