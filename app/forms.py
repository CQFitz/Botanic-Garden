# app/forms.py

import flask
from flask_wtf import FlaskForm
from wtforms import (BooleanField, HiddenField, StringField, SubmitField, TextAreaField, SelectField)
from wtforms.validators import (DataRequired, Length, Optional)
from wtforms.widgets import html_params


from app import models

app = flask.current_app


class Famillies(FlaskForm):
    family_name = StringField('The name of plant family', [DataRequired()])
    family_details = TextAreaField('Family Plant details', [
        Length(min=3, max=2048, message='Details must be at least %(min)d characters' 'long and %(max)d at most.'),
        DataRequired(message='Details must not be empty.')
    ])
    family_description = TextAreaField('Family Plant description', [
        Length(min=3, max=2048, message='Description must be at least %(min)d characters' 'long and %(max)d at most.'),
        DataRequired(message='Description must not be empty.')
    ])


class PlantHierarchies(FlaskForm):
    plant_hierarchy_name = StringField("Plant Hierarchy Name", [DataRequired()])
    plant_hierarchy_details = TextAreaField("Plant Hierarchy Details", [
        Length(min=3, max=2048, message='Details must be at least %(min)d characters' 'long and %(max)d at most.'),
        DataRequired(message='Details must not be empty.')
    ])
    parent_plant_hierarchy_id = SelectField("Related to Plant Hierarchy", [Optional()])


class Locations(FlaskForm):
    location_name = StringField("Location name", [DataRequired()])
    location_position = StringField("Location position", [DataRequired()])


class PlantsLocations(FlaskForm):
    plant_id = SelectField("plant id", [DataRequired()])
    location_id = SelectField("location id", [DataRequired()])


class Plants(FlaskForm):
    plant_hierarchy_id = SelectField('From Hierarchy', coerce=int)
    family_id = SelectField('From Family', coerce=int)
    plant_details = TextAreaField("Plant Details", [
        Length(min=3, max=2048, message='Details must be at least %(min)d characters' 'long and %(max)d at most.'),
        DataRequired(message='Details must not be empty.')
    ])
    # I do not know if this is needed
    location_id = SelectField("Select Location", [Optional()])
    location_name = StringField("Location name", [Optional()])
    location_position = StringField("Location position", [Optional()])


class RemoveForm(FlaskForm):
    remove = SubmitField("Remove")