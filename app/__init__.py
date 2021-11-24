# app/__init__.py

import flask

from config import app_config
from .views import register_views

def create_app(config_name):
    app = flask.Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    from app import models

    from app.database import db_session

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    register_views(app)

    @app.route('/')
    def botanic_garden():
        return flask.render_template('site.html', app=app)

    return app