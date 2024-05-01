"""
Define the database models.
"""

from Moodle_rf import db
import hashlib

class users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    degree_id = db.Column(db.Integer, db.ForeignKey('degrees.id'))
    role = db.Column(db.String(64), nullable=False, default='student')
    
    def set_password(self, password):
        self.password = hashlib.sha256(password.encode()).hexdigest()
        
    def check_password(self, password):
        return self.password == hashlib.sha256(password.encode()).hexdigest()

class courses(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    credit = db.Column(db.Integer, nullable=False)

class degrees(db.Model):
    __tablename__ = 'degrees'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    users = db.relationship('users', backref='degrees', lazy=True)

class mycourses(db.Model):
    __tablename__ = 'mycourses'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)

class approved_degrees(db.Model):
    __tablename__ = 'approved_degress'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    degree_id = db.Column(db.Integer, db.ForeignKey('degrees.id'), nullable=False)

class events(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
