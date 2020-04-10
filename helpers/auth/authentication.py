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

api_url = "https://localhost:5000/api/v1/"


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

                    for value in response['values']:
                        if user_data.email == value["email"]:
                            if value['location']:  # pragma: no cover
                                check_and_add_location(
                                    value['location']['name'])
                    notification_settings = NotificationModel(
                        user_id=user_data.id)
                    notification_settings.save()
                except Exception as e:  # noqa
                    db_session.rollback()
        except SQLAlchemyError:  # pragma: no cover
            pass
        return True


Auth = Authentication()
