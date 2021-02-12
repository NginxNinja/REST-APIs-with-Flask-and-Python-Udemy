from werkzeug.security import safe_str_cmp
from user import User

def authenticate(username,password):
    user = User.find_by_username(username)
    # safe_str_cmp() function will compare the two strings and gonna work from the old versions of Python, servers, etc.
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    user_id = payload["identity"]
    return User.find_by_id(user_id)