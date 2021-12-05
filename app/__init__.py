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

        get_family=None
        get_hieararchies=None
        get_parent_hieararchies=None
        get_main_hieararchy=None
        get_main_sub_hieararchy=None

        try:
            get_family = models.Famillies.by_id(random_plant.family_id)
            get_hieararchies = models.PlantHierarchies.query.filter_by(parent_plant_hierarchy_id=random_plant.plant_hierarchy_id)
            get_parent_hieararchies = models.PlantHierarchies.query.filter_by(plant_hierarchy_id=random_plant.plant_hierarchy_id)
            
            get_main_sub_hieararchy = models.PlantHierarchies.query.filter_by(parent_plant_hierarchy_id=random_plant.plant_hierarchy_id).first()
            get_main_hieararchy = models.PlantHierarchies.query.filter_by(plant_hierarchy_id=get_main_sub_hieararchy.parent_plant_hierarchy_id).first()
        
        except:
            get_main_sub_hieararchy = models.PlantHierarchies.query.filter_by(plant_hierarchy_id=random_plant.plant_hierarchy_id).first()
            get_main_hieararchy = models.PlantHierarchies.query.filter_by(plant_hierarchy_id=get_main_sub_hieararchy.parent_plant_hierarchy_id).first()
        
            ''

        return flask.render_template('site.html', plant=random_plant, family=get_family, hierarchies=get_hieararchies, parent_hierarchies=get_parent_hieararchies, hierarchy=get_main_hieararchy)

    return app