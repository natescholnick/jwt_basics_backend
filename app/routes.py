from app import app, db
from flask import redirect, url_for, request, jsonify
from app.models import User
import time
import jwt


@app.route('/')
@app.route('/index')
def index():
    return ''


@app.route('/api/register', methods=['GET', 'POST'])
def register():
    try:
        token = request.headers.get('token')
        print(token)

        # decode token back to dict
        data = jwt.decode(
            token,
            app.config['SECRET_KEY'],
            algorithm=['HS256']
        )
        print(data)

        # create user and save to db
        user = User(email=data['email'])
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()

        return jsonify({ 'messge': 'Success!'})

    except:
        return jsonify({'message': 'User not created.'})



@app.route('/api/login', methods=['GET', 'POST'])
def login():
    try:
        token = request.headers.get('token')
        print(token)

        data = jwt.decode(
            token,
            app.config['SECRET_KEY'],
            algorithm=['HS256']
        )
        print(data)

        user = User.query.filter_by(email=data['email']).first()

        if not user or not user.check_password(data['password']):
            return jsonify({'message': 'Invalid credentials'})

        return jsonify({'message': 'Success', 'token': user.get_token()})

    except:
        return jsonify({'message': 'Failure to login'})

@app.route('/api/data', methods=['GET', 'POST'])
def data():
    try:
        token = request.headers.get('token')
        print(token)

        # get user_id or nothing
        user = User.verify_token(token)

        # if user does not exist, return a failure, otherwise return data
        if not user:
            return jsonify({'message': 'Invalid user'})

        data = {
            'name': 'Stupid dumb idiot',
            'age': 'Probably like 14 or something'
        }

        return jsonify({'info': data})

    except:
        return jsonify({'message': 'Invalid token'})
