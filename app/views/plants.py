import flask
from app import database, forms, models


app = flask.current_app
bp = flask.Blueprint('plants', __name__)


@bp.route('/plants/')
def plants():
    query = models.Plants.query.all()
    url = flask.url_for('plants.new_plant')
    if not query:
        flask.flash(flask.Markup("It Seems to be there is nothing in the Plant database. Try to add something"), 'warning')
        return flask.redirect(url)

    return flask.render_template('plants/plants.html', plants_query=query)


@bp.route('/plants/view/<plant_id>', methods=['GET', 'POST'])
def view_plant(plant_id):
    query = models.Plants.by_id(plant_id)
    if not query:
        flask.abort(404)

    related_family_info = models.Famillies.by_id(query.family_id)
    related_hierarchy_info = models.PlantHierarchies.by_id(query.plant_hierarchy_id)
    location = models.PlantLocations.by_plant_id(plant_id)
    plant_from_same_family = models.Plants.related_family_plant(query.family_id)
    plant_from_same_hierarchy = models.Plants.related_hierarchy_plant(query.plant_hierarchy_id)

    return flask.render_template(
        'plants/plant.html',
        plant=query,
        family=related_family_info,
        hierarchy=related_hierarchy_info,
        same_family_plant=plant_from_same_family,
        same_hierarchy_plant=plant_from_same_hierarchy,
        location=location
        )


@bp.route('/plants/new', methods=['GET', 'POST'])
def new_plant():
    form = forms.Plants(flask.request.form)
    location_query = None
    url = flask.url_for('plants.new_plant')

    form.plant_hierarchy_id.choices = [('0','Please Choose')] + [(g.plant_hierarchy_id, g.plant_hierarchy_name) for g in models.PlantHierarchies.query.order_by('plant_hierarchy_name')]
    form.family_id.choices = [('0','Please Choose')] + [(g.family_id, g.family_name) for g in models.Famillies.query.order_by('family_name')]
    form.location_id.choices = [('0','Please Choose Or Create New')] + [(g.location_id, g.location_name) for g in models.Locations.query.order_by('location_name')]

    if flask.request.method == 'POST' and form.validate():
        if form.plant_hierarchy_id.data == 0 or form.family_id.data == 0:
            flask.flash(flask.Markup("Plase Select the right selectable section"), 'danger')
            return flask.render_template('plants/new_plant.html', form=form)

        elif form.location_name.data == '' and form.location_position.data == '' and form.location_id.data == 0:
            flask.flash(flask.Markup("Location name and location position not filled, you can fill it later"), 'info')

        elif form.location_name.data != '' and form.location_position.data != '':
            location_query = models.Locations(
                form.location_name.data,
                form.location_position.data,
            )

            database.db_session.add(location_query)
            database.db_session.commit()

        plant_query = models.Plants(
            form.plant_hierarchy_id.data,
            form.family_id.data,
            form.plant_details.data,
        )
        
        database.db_session.add(plant_query)
        database.db_session.commit()
        
        if location_query:
            plant_location_query = models.PlantLocations(
                plant_query.plant_id,
                location_query.location_id
            )
            database.db_session.add(plant_location_query)
            database.db_session.commit()

        else:
            plant_location_query = models.PlantLocations(
                plant_query.plant_id,
                form.location_id.data
            )
            database.db_session.add(plant_location_query)
            database.db_session.commit()
        
        flask.flash(flask.Markup("Successfully add new plant!"), 'success')
        return flask.redirect(url)

    return flask.render_template('plants/new_plant.html', form=form)


@bp.route('/plants/edit/<plant_id>', methods=['GET', 'POST'])
def update_plant(plant_id):
    form = forms.Plants(flask.request.form)
    remove_form = forms.RemoveForm()

    query = models.Plants.by_id(plant_id)
    try:
        location_query = models.PlantLocations.by_plant_id(query.plant_id)
    except:
        location_query = None

    hierarchies_query = models.PlantHierarchies.by_id(query.plant_hierarchy_id)
    famillies_query = models.Famillies.by_id(query.family_id)

    url = flask.url_for('plants.view_plant', plant_id=plant_id)

    form.plant_hierarchy_id.choices = [(hierarchies_query.plant_hierarchy_id, '( SELECTED ) | ' + hierarchies_query.plant_hierarchy_name)] + [(g.plant_hierarchy_id, g.plant_hierarchy_name) for g in models.PlantHierarchies.query.order_by('plant_hierarchy_name')]
    form.family_id.choices = [(famillies_query.family_id, '( SELECTED ) | ' + famillies_query.family_name)] + [(g.family_id, g.family_name) for g in models.Famillies.query.order_by('family_name')]
    if location_query == None:
        form.location_id.choices = [('0','Please Choose Or Create New')] + [(g.location_id, g.location_name) for g in models.Locations.query.order_by('location_name')]
    else:
        form.location_id.choices = [(location_query.location_id, '( SELECTED ) | ' + location_query.location_name)] + [('0','Please Choose Or Create New')] + [(g.location_id, g.location_name) for g in models.Locations.query.order_by('location_name')]

    if flask.request.method == 'POST' and form.validate():
        if form.plant_hierarchy_id.data == 0 or form.family_id.data == 0 or form.plant_hierarchy_id.data == '':
            flask.flash(flask.Markup("Plase Select the right selectable section"), 'danger')
            return flask.render_template('plants/edit_plant.html', form=form)

        elif form.location_name.data == '' and form.location_position.data == '' and form.location_id.data == 0:
            flask.flash(flask.Markup("Location name and location position not filled, you can fill it later"), 'info')

        elif form.location_name.data != '' and form.location_position.data != '':
            location_query = models.Locations(
                form.location_name.data,
                form.location_position.data,
            )

            database.db_session.add(location_query)
            database.db_session.commit()

        query.plant_hierarchy_id = form.plant_hierarchy_id.data
        query.family_id = form.family_id.data
        query.plant_details = form.plant_details.data

        database.db_session.add(query)
        database.db_session.commit()

        location_query = None
        if not location_query: # Create new Plant Location
            plant_location_query = models.PlantLocations(
                plant_id,
                form.location_id.data
            )

            database.db_session.add(plant_location_query)
            database.db_session.commit()
            return flask.redirect(url)

        elif form.location_id.data != 0: # Update Plant Location
            plant_location_query = models.PlantLocations.query.filter_by(plant_id=plant_id).first()

            plant_location_query.plant_id = plant_id
            plant_location_query.plant_location_id = form.location_id.data
            
            database.db_session.add(plant_location_query)
            database.db_session.commit()
            return flask.redirect(url)

        return flask.redirect(url)

    form.plant_details.data = query.plant_details

    return flask.render_template('plants/edit_plant.html', form=form, remove_form=remove_form, query=query)