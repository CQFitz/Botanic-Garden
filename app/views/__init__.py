# app/view/__init__.py

import flask

# from app.views import (famillies,)
from app.views import (
    famillies,
    plants,
    plant_hierarchies,
    locations,
)

def register_views(flask_app):
    flask_app.register_blueprint(famillies.bp)
    flask_app.register_blueprint(plants.bp)
    flask_app.register_blueprint(plant_hierarchies.bp)
    flask_app.register_blueprint(locations.bp)
