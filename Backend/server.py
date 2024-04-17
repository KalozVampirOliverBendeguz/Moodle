from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for
from flask import Flask, jsonify
from models import db, User, Course, Degree, MyCourse, ApprovedDegree, Event

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/moodle'
app.template_folder = 'Frontend'
db.init_app(app)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            
            return redirect(url_for('index')) 
        else:
            
            return render_template('login.html', message='Invalid username or password.')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        password = request.form['password']
        user = User(username=username, name=name, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))  
    return render_template('registration.html')


if __name__ == '__main__':
    app.run(debug=True)