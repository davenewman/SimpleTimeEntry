import os

db_info = {
    'filename': os.path.join(os.getcwd(), 'TimeEntry.db'),
    'tasks': [('Overhead', 'Tasks such as email, preparing for sessions, completing documents, and other duties as assigned', 'Overhead - '),
              ('Training', 'Compliance, mandatory, and/or pre-approved or assigned by manager', 'Training - '),
              ('Other', 'This is the task description', 'Other - '),
              ('Shell MDIS', 'Work pertaining to the Shell MDIS project', 'Shell MDIS - '),
              ('Shell OWIRS', 'Work pertaining to the Shell OWIRS project', 'EDP/LRP Tooling - '),
              ('Low Bay ME', 'ME tasks - low bay', 'ME Low Bay - '),
              ('High Bay ME','ME tasks - high bay','ME High Bay - '),
              ('CDM ME','ME tasks - CDM','ME CDM - '),]
}
