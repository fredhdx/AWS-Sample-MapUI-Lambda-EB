from MapService import users, login_manager
from flask_login import UserMixin
from bson.objectid import ObjectId


@login_manager.user_loader
def load_user(id):
    '''
    Load user for login manager.
    '''
    u = User.get_user_by_id(id)
    if u is None:
        return None
    return u

class User(UserMixin):
    '''
    User class for login manager.
    '''
    def __init__(self, username, password, email, id):
        self.username = username
        self.password = password
        self.email = email
        self.id = id

    @staticmethod
    def get_user(email):
        user = users.find_one({"email": email})
        if user is None:
            return None
        else:
            return User(user['username'], user['password'], user['email'], user['_id'])

    @staticmethod
    def get_user_by_id(id):
        user = users.find_one({"_id": ObjectId(id)})
        if user is None:
            return None
        else:
            return User(user['username'], user['password'], user['email'], user['_id'])
