"""This package is Flask HTTP REST API Template template that already has the database bootstrap
implemented and also all feature related with the user authentications.
Application features:
    Python 3.7
    Flask
    PEP-8 for code style
This module contains the factory function 'create_app' that is
responsible for initializing the application according
to a previous configuration.
"""

import os

from flask import Flask, Blueprint
from flask_restful import Api
from flask_jwt_extended import JWTManager


def create_app(test_config=None):
    """This function is responsible to create a Flask instance according
    a previous setting passed from environment. In that process, it also
    initialise the database source.
    Parameters:
        test_config (dict): settings coming from test environment
    Returns:
        flask.app.Flask: The application instance
    """

    app = Flask(__name__)
    api_bp = Blueprint('api', __name__)
    api = Api(api_bp)

    load_config(app, test_config)

    init_instance_folder(app)
    init_database(app)
    init_blueprints(app)
    init_commands(app)
    init_jwt_manager(app)

    return app


def load_config(app: Flask, test_config):
    """Load the application's config
    Parameters:
        app (flask.app.Flask): The application instance Flask that'll be running
        test_config (dict):
    """

    if os.environ.get("FLASK_ENV") == 'development' or test_config.get("FLASK_ENV") == 'development':
        app.config.from_object('api.config.Development')

    elif test_config.get('TESTING'):
        app.config.from_mapping(test_config)

    else:
        app.config.from_object('app.config.Production')


def init_instance_folder(app: Flask):
    """Ensure the instance folder exists.
    Parameters:
        app (flask.app.Flask): The application instance Flask that'll be running
    """

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


def init_database(app):
    """Responsible for initializing and connecting to the database
    to be used by the application.
    Parameters:
        app (flask.app.Flask): The application instance Flask that'll be running
    """

    from .database import init
    init(app)


def init_blueprints(app: Flask):
    """Registes the blueprint to the application.
    Parameters:
        app (flask.app.Flask): The application instance Flask that'll be running
    """

    # error handlers
    from .resources.handlers import register_handler
    register_handler(app)

    # error Handlers
    from .resources import index, auth, account, product
    app.register_blueprint(index.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(account.bp)
    app.register_blueprint(product.bp)


def init_commands(app):
    from api.commands import register_commands
    register_commands(app)


def init_jwt_manager(app):
    from .authentication import init
    jwt = JWTManager(app)
    init(jwt)
