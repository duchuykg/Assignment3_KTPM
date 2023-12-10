from test_reply_in_forum import *
from test_upload_private_file import *
import json

with open('./input/upload_file_input.json', encoding='UTF-8') as f:
    data = json.load(f)
    upload_file = test_upload_private_file(data)
    print(upload_file.run())


"""with open('./input/compatibility_input.json', encoding='UTF-8') as f:
    data = json.load(f)
    compatibility = test_compatibility(data)
    print(compatibility.run())"""
