from user import User
from werkzeug.security import safe_str_cmp

users = [
    User(1, 'bob', 'qwerty')
]

username_mapping = {user.username: user for user in users}

userid_mapping = {user.id: user for user in users}


def authenticate(username, password):
    user = username_mapping.get(username)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    userid = payload['identity']
    return userid_mapping.get(userid)