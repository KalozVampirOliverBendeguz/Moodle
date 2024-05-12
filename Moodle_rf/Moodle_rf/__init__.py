"""
The flask application package.
"""

from flask import Flask
from Moodle_rf.database import db
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'az-egyedi-titkos-kulcsod'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/moodle'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

socketio = SocketIO(app)
db.init_app(app)

import Moodle_rf.views
