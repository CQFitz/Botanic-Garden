# app/__init__.py

import flask

from config import app_config
from .views import register_views
from  sqlalchemy.sql.expression import func, select

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
        random_plant = models.Plants.query.order_by(func.random()).first()
        get_family = models.Famillies.by_id(random_plant.family_id)
        get_hieararchies = models.PlantHierarchies.query.filter_by(plant_hierarchy_id=random_plant.plant_hierarchy_id)
        get_parent_hieararchies = models.PlantHierarchies.query.filter_by(parent_plant_hierarchy_id=random_plant.plant_hierarchy_id)
        return flask.render_template('site.html', family=get_family, hierarchies=get_hieararchies, parent_hierarchies=get_parent_hieararchies)

    return app