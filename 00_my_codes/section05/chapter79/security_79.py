from werkzeug.security import safe_str_cmp
from user_72 import User

#-- Inefficient and manual way
# users = {
#     {
#         "id": 1,
#         "username": "bob",
#         "password": "asdf"
#     }
# }

#-- More concise and effective way
users = [
    User(1, "bob", "asdf")
    ]

#-- Inefficient and manual way
# username_mapping = {
#     "bob": {
#         "id": 1,
#         "username": "bob",
#         "password": "asdf"
#     }
# }

#-- More concise and effective way
username_mapping = {u.username: u for u in users}

#-- Inefficient and manual way
# userid_mapping = {
#     1: {
#         "id": 1,
#         "username": "bob",
#         "password": "asdf"
#     }
# }

#-- More concise and effective way
userid_mapping = {u.id: u for u in users}

def authenticate(username,password):
    # dict.get() Return the value for key if key is in the dictionary, else default. If default is not given, it defaults to None, so that this method never raises a KeyError.
    user = username_mapping.get(username, None)
    # safe_str_cmp() function will compare the two strings and gonna work from the old versions of Python, servers, etc.
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    user_id = payload["identity"]
    return userid_mapping.get(user_id, None)