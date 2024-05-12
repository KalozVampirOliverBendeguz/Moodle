"""
This script runs the Moodle_rf application using a development server.
"""
from flask import Flask
from os import environ
from Moodle_rf import app, socketio


if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    socketio.run(app, HOST, PORT)
