from flask import Flask, render_template, Response
from flask_graphql import GraphQLView
from flask_cors import CORS
from flask_json import FlaskJSON

from config import config
from helpers.database import db_session
from schema import schema
from helpers.auth.authentication import Auth
from utilities.file_reader import read_log_file


def create_app(config_name):
    app = Flask(__name__)
    CORS(app)
    FlaskJSON(app)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    @app.route("/", methods=['GET'])
    def index():
        return render_template('index.html')

    @app.route("/logs", methods=['GET'])
    @Auth.user_roles('Admin', 'REST')
    def logs():
        response = None
        log_file = 'emr.err.log'
        try:
            open(log_file)  # trigger opening of file
            response = Response(read_log_file(log_file), mimetype='text')
        except FileNotFoundError:  # pragma: no cover
            message = 'Log file was not found'
            response = Response(message, mimetype='text', status=404)
        return response

    app.add_url_rule(
        '/emr',
        view_func=GraphQLView.as_view(
            'emr',
            schema=schema,
            graphiql=True   # for having the GraphiQL interface
        )
    )

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app
