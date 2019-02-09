from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from instance.config import app_config
from webargs.flaskparser import use_args, use_kwargs, parser, abort


# initialize sql-alchemy
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__,  instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    return app

@parser.error_handler
def handle_request_parsing_error(err, req, schema):
    """webargs error handler that uses Flask-RESTful's abort function to return
    a JSON error response to the client.
    """
    abort(422, errors=err.messages)

