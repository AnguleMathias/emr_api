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
from utilities.utility import StateType

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
