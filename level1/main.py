from test_reply_in_forum import *
from test_upload_private_file import *
from test_submit_assignment import *
from test_submit_quiz import *

import json

with open('./input/submit_quiz.json', encoding='UTF-8') as f:
    data = json.load(f)  
    submit_quiz = test_submit_quiz(data)
    print(submit_quiz.run())
    
with open('./input/submit_assignment.json', encoding='UTF-8') as f:
    data = json.load(f)  
    submit_assignment = test_submit_assignment(data)
    print(submit_assignment.run())

with open('./input/upload_file_input.json', encoding='UTF-8') as f:
    data = json.load(f)
    upload_file = test_upload_private_file(data)
    print(upload_file.run())