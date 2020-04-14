import json
import jwt
import os

from flask import request, jsonify
from functools import wraps

import requests
from graphql import GraphQLError

from api.user.models import User
from api.role.models import Role
from helpers.connection.connection_error_handler import handle_http_error
from helpers.database import db_session
from utilities.utility import StateType

api_url = "https://localhost:8000/emr"


class Authentication:
    def get_token(self):
        try:
            token = request.headers['Authorization'].split()[1]
        except BaseException:
            token = None
        return token

    def decode_token(self):
        try:
            auth_token = self.get_token()
            if auth_token is None:
                return jsonify({
                    'message':
                    'Invalid token. Please Provide a valid token!'
                }), 401

            payload = jwt.decode(auth_token, verify=False)
            self.user_info = payload['UserInfo']
            return payload['UserInfo']
        except jwt.ExpiredSignatureError:
            return jsonify({
                'message': 'Signature expired. Please log in again.'
            }), 401
        except jwt.InvalidTokenError:
            return jsonify({
                'message':
                'Invalid token. Please Provide a valid token!'
            }), 401

    def get_user_details_from_api(self, email, *expected_args):
        try:
            headers = {"Authorization": 'Bearer ' + self.get_token()}
            data = requests.get(
                api_url + "users?email=%s"
                % email, headers=headers)
            response = json.loads(data.content.decode("utf-8"))

            return response
        except requests.exceptions.ConnectionError:
            message = "Failed internet connection"
            status = 408
            handle_http_error(message, status, expected_args)

        if 'error' in response:
            message = response['error']
            status = 401
            if(message == "invalid token"):
                message = "You don't have a valid credentials to perform this action"
                handle_http_error(message, status, expected_args)
            else:
                handle_http_error(message, status, expected_args)

    def save_user(self,  email, *expected_args):
        try:
            email = self.user_info['email']
            name = self.user_info['name']
            picture = self.user_info['picture']
            user = User.query.filter_by(email=email).first()
            role = Role.query.filter_by(role='Default User').first()
            if not role:
                role = Role(role='Default User')
                role.save()

            if not user:
                try:
                    response = self.get_user_details_from_api(
                        email, *expected_args)
                    user_data = User(email=email, name=name, picture=picture)
                    user_data.roles.append(role)

                except Exception as e:  # noqa
                    db_session.rollback()
        except SQLAlchemyError:  # pragma: no cover
            pass
        return True

    def user_roles(self, *expected_args):  # noqa: C901
        """ User roles """

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                user_data = self.decode_token()
                if type(user_data) is dict:
                    email = user_data['email']

                    try:
                        user = User.query.filter_by(email=email).first()
                    except Exception:
                        raise GraphQLError("The database cannot be reached")

                    if user and user.state != StateType.active:  # pragma: no cover # noqa
                        raise GraphQLError(
                            "Your account is not active, please contact an admin")  # noqa

                    if not user:
                        self.save_user(email, *expected_args)
                        user = User.query.filter_by(email=email).first()
                    if user.roles and user.roles[0].role in expected_args:
                        return func(*args, **kwargs)
                    else:
                        message = (
                            'You are not authorized to perform this action')
                        status = 401
                        handle_http_error(message, status, expected_args)

                else:
                    raise GraphQLError(user_data[0].data)

            return wrapper

        return decorator


Auth = Authentication()
