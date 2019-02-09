from functools import wraps
from flask import abort,request, current_app as app
import jwt
from app.models import User


def authorize(f):
    @wraps(f)
    def decorated_function(user):
        try:
            token = request.cookies.get('token')
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            userId = payload['id']
            user = User.query.get(userId)
        except Exception as e:
            abort(401)

        return f(user)

    return decorated_function
