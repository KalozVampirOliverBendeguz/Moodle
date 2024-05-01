from functools import wraps
from flask_jwt_extended import get_jwt_identity, jwt_required
from Moodle_rf.models import users
from passlib.hash import sha256_crypt
from datetime import datetime, timedelta
import jwt

def hash_password(password):
    return sha256_crypt.hash(password)

def create_token(user):
    token_payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(hours=1)
    }
    token = jwt.encode(token_payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token

def authenticate(username, password):
    user = users.query.filter_by(username=username).first()
    if user and sha256_crypt.verify(password, user.password):
        return user

def check_student_role(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = users.query.get(current_user_id)
        if user.role == 'student':
            return fn(*args, **kwargs)
        else:
            return jsonify({"msg": "Unauthorized"}), 401
    return wrapper