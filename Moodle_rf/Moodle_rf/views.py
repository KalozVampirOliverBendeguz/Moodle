"""
Routes and views for the flask application.
"""
from functools import wraps
from math import e
from flask import render_template, redirect, url_for, flash, session, request, jsonify, make_response
from datetime import datetime
from Moodle_rf import app
from Moodle_rf.forms import LoginForm, RegistrationForm
from Moodle_rf.models import users, mycourses, courses, degrees, approved_degrees
from Moodle_rf.models import events
from Moodle_rf.database import db
from sqlalchemy.orm import join, selectinload
import hashlib

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('You must be logged in to access this page.', 'error')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/', methods=['GET', 'POST'])
def home():
    login_form = LoginForm()
    
    if login_form.validate_on_submit():
        user = users.query.filter_by(username=login_form.username.data).first()
        if user is not None and user.password == hashlib.sha256(login_form.password.data.encode()).hexdigest():
            flash('Login successful!', 'success')
            response = make_response(redirect(url_for('moodle')))
            response.set_cookie('user_id', str(user.id))
            session['role'] = user.role
            return response
        else:
            flash('Login unsuccessful. Please check your credentials and try again.', 'error')
            
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
        login_form=login_form
    )

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    form.degree.choices = [(degree.id, degree.name) for degree in degrees.query.all()]  
    if form.validate_on_submit():
        hashed_password = hashlib.sha256(form.password.data.encode()).hexdigest()
        user = users(username=form.username.data, name=form.name.data, password=hashed_password, degree_id=form.degree.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )
@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/moodle', methods=['GET'])
@login_required
def moodle():
    if session.get('role') not in ('admin', 'student'): 
        flash('You are not authorized to access this page.', 'error')
        return redirect(url_for('home'))
    event_list = events.query.all()
    user_id = request.cookies.get('user_id')
    if not user_id:
        flash('You are not logged in.', 'error')
        return redirect(url_for('home'))  
    degree_id = request.args.get('degree_filter')
    if degree_id:
        filtered_courses = (
            courses.query
            .join(approved_degrees, courses.id == approved_degrees.course_id)
            .join(degrees, approved_degrees.degree_id == degrees.id)
            .filter(degrees.id == degree_id)
            .all()
        )
    else:
        filtered_courses = courses.query.all()
    print("User ID cookie:", user_id)
    return render_template('moodle.html', courses=filtered_courses, degrees=degrees.query.all(), events=event_list)




@app.route('/logout', methods=['POST'])
@login_required
def logout():
    return redirect(url_for('home'))

@app.route('/enroll', methods=['POST'])
@login_required
def enroll():
    if session.get('role') not in ('admin', 'student'): 
        flash('You are not authorized to access this page.', 'error')
        return redirect(url_for('home'))
    user_id = request.cookies.get('user_id')
    if not user_id:
        flash('You are not logged in.', 'error')
        return redirect(url_for('home'))
    course_id = request.form.get('course_id')
    enrolled_user = users.query.filter_by(id=user_id).join(degrees).join(approved_degrees).filter(approved_degrees.course_id == course_id).first()
    if not enrolled_user:
        flash('You are not eligible to enroll in this course.', 'error')
    else:
        enrollment_exists = mycourses.query.filter_by(user_id=user_id, course_id=course_id).first()
        if enrollment_exists:
            flash('You have already enrolled in this course.', 'error')
        else:
            new_enrollment = mycourses(user_id=user_id, course_id=course_id)
            db.session.add(new_enrollment)
            db.session.commit()
            flash('Enrollment successful!', 'success')
    print("User ID cookie:", user_id)
    return redirect(url_for('moodle'))

@app.route('/mycourses', methods=['GET'])
@login_required
def my_courses():
    if session.get('role') not in ('admin', 'student'): 
        flash('You are not authorized to access this page.', 'error')
        return redirect(url_for('home'))
    user_id = request.cookies.get('user_id')
    if not user_id:
        flash('You are not logged in.', 'error')
        return redirect(url_for('home'))
    user_courses = (
        courses.query
        .join(mycourses, courses.id == mycourses.course_id)
        .filter(mycourses.user_id == user_id)
        .all()
    )
    print("User ID cookie:", user_id)
    course_names = [course.name for course in user_courses]
    return render_template('mycourses.html', courses=course_names)


@app.route('/course_enrollments')
@login_required
def course_enrollments():
    if session.get('role') not in ('admin', 'student'): 
        flash('You are not authorized to access this page.', 'error')
        return redirect(url_for('home'))
    user_id = request.cookies.get('user_id') 
    if not user_id:
        flash('You are not logged in.', 'error')
        return redirect(url_for('home'))
    course_id = request.args.get('course_id')
    enrolled_users = (
        users.query
        .join(mycourses, users.id == mycourses.user_id)
        .join(courses, mycourses.course_id == courses.id)
        .filter(courses.id == course_id)
        .all()
    )
    print("User ID cookie:", user_id)
    user_list = [user.name for user in enrolled_users]
    return jsonify({'users': user_list})



@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if session.get('role') != 'admin': 
        flash('You are not authorized to access this page.', 'error')
        return redirect(url_for('home'))
    
    if request.method == 'POST':
    
        code = request.form.get('code')
        name = request.form.get('name')
        credit = request.form.get('credit')
        degree_id = request.form.get('degree')
        new_course = courses(code=code, name=name, credit=credit)
        db.session.add(new_course)
        db.session.commit()
        flash('New course added successfully!', 'success')
        new_approved_degree = approved_degrees(course_id=new_course.id, degree_id=degree_id)
        db.session.add(new_approved_degree)
        db.session.commit()
        flash('Course added to approved degrees!', 'success')
        return redirect(url_for('admin'))

    all_courses = courses.query.all()
    return render_template('admin.html', courses=all_courses, degrees=degrees.query.all())
