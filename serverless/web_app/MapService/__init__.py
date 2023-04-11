from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_pymongo import PyMongo
from flask import Flask
import json

config_json = json.load(open("./MapService/config/config.json"))

app = Flask(__name__)
app.config['SECRET_KEY'] = config_json["SECRET_KEY"]
app.config["MONGO_URI"] = config_json["ATLAS_MONGO_URI"]
# app.config["MONGO_URI"] = config_json["LOCAL_MONGO_URI"]

mongo = PyMongo(app)
users = mongo.db.user
MAPBOX_ACCESS_TOKEN = config_json["MAPBOX_ACCESS_TOKEN"]
MAPBOX_STYLE = config_json["MAPBOX_STYLE"]
DATABASE_NAME = config_json["DATABASE_NAME"]
ATLAS_MONGO_URI = config_json["ATLAS_MONGO_URI"]

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from MapService import routes
