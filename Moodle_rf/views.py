"""
Routes and views for the flask application.
"""

from math import e
from flask import render_template, redirect, url_for, flash, session, request, jsonify
from datetime import datetime
from Moodle_rf import app
from Moodle_rf.forms import LoginForm
from Moodle_rf.models import users, mycourses, courses, degrees, approved_degrees
from Moodle_rf.models import events
from Moodle_rf.database import db
from sqlalchemy.orm import join, selectinload



@app.route('/', methods=['GET', 'POST'])
def home():

    login_form = LoginForm()
    
    if login_form.validate_on_submit():
        user = users.query.filter_by(username=login_form.username.data).first()
        if user is not None and user.check_password(login_form.password.data):
            flash('Login successful!', 'success')
            session['user_id'] = user.id
            return redirect(url_for('moodle'))
        else:
            flash('Login unsuccessful. Please check your credentials and try again.', 'error')
            

    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
        login_form=login_form,
    )

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
def moodle():
    event_list=events.query.all()
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
    return render_template('moodle.html',courses=filtered_courses, degrees=degrees.query.all(), events=event_list)



@app.route('/logout', methods=['POST'])
def logout():
    return redirect(url_for('home'))

@app.route('/enroll', methods=['POST'])
def enroll():
    user_id = session.get('user_id') 
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

    return redirect(url_for('moodle'))

@app.route('/mycourses', methods=['GET'])
def my_courses():
    user_id = session.get('user_id')
    user_courses = (
        courses.query
        .join(mycourses, courses.id == mycourses.course_id)
        .filter(mycourses.user_id == user_id)
        .all()
    )
    course_names = [course.name for course in user_courses]
    return render_template('mycourses.html', courses=course_names)


@app.route('/course_enrollments')
def course_enrollments():
    course_id = request.args.get('course_id')
    enrolled_users = (
        users.query
        .join(mycourses, users.id == mycourses.user_id)
        .join(courses, mycourses.course_id == courses.id)
        .filter(courses.id == course_id)
        .all()
    )
    user_list = [user.name for user in enrolled_users]
    return jsonify({'users': user_list})
