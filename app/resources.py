from flask_restplus import Resource
from flask import request
from app.models import User
from webargs import fields, validate, ValidationError
from webargs.flaskparser import use_args, use_kwargs, parser, abort
from email_validator import validate_email
from flask import current_app as app 
import jwt
from app.authorization import authorize
from flask import jsonify
from datetime import datetime, timedelta

gen_token = lambda userId, expiration: jwt.encode({'id': userId, 'exp': expiration}, app.config['SECRET_KEY'],  algorithm='HS256').decode('utf-8')

class UserResource(Resource):

    userLoginArgs = {"email": fields.Str(required=True),
                     "password": fields.Str(validate=validate.Length(min=6))}
    
    @use_args(userLoginArgs)
    def get(self, args):
        email = args['email']
        password = args['password']
        user = User.query.filter_by(email=email).first()

        if user is None or not user.check_password_hash(password):
            return {'errors': 'email or password is incorrect'}, 400
        
        response = jsonify({'success': True})
        response.set_cookie(key='token', value= gen_token(user.id, datetime.utcnow() + timedelta(days=1000)))
        return response

    createUserArgs = {"fullname" : fields.Str(required=True),
                      "email": fields.Str(required=True),
                      "password": fields.Str(validate=validate.Length(min=6))}

    @use_args(createUserArgs)
    def post(self, args):
        fullname = args['fullname']
        email = args['email']
        password = args['password']

        try:
            validate_email(email)
        except:
            print("boo")
            return {'errors': {'email': 'invalid email'}}, 400

        if User.query.filter_by(email=email).first() is not None:
            print('hello')
            return {'errors': {'email': 'email already exists'}}, 400   

        user = User(fullname, email, password)
        user.save()

        response = jsonify({'success': True})
        response.set_cookie('token',  gen_token(user.id, datetime.utcnow() + timedelta(days=1000)))
        return response 

class Logout(Resource):
    def post(self):
        response = jsonify({"success": True})
        response.set_cookie('token', '', expires=0)
        return response 

class ProtectedResource(Resource):
    @authorize
    def get(user):
        print('helloworld')
        print(user)
        return {}

