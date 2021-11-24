import flask
from app import database, forms, models

app = flask.current_app
bp = flask.Blueprint('locations', __name__)


@bp.route('/locations/')
def locations():
    query = models.Locations.query.all()
    url = flask.url_for('locations.new_location')
    if not query:
        flask.flash(flask.Markup("It Seems to be there is nothing in the locations database. Try to add something"), 'warning')
        return flask.redirect(url)

    form = None
    test = database.db_session.query(models.Famillies).join(models.Plants.family)

    return flask.render_template('locations/locations.html', locations_query=query, test=test)


@bp.route('/locations/view/<location_id>', methods=['GET', 'POST'])
def view_location(location_id):
    query = models.Locations.by_id(location_id)

    if not query:
        flask.abort(404)

    form = None

    url = flask.url_for('locations.view_location', location_id=query.location_id)

    return flask.render_template('locations/location.html', location=query)


@bp.route('/locations/new', methods=['GET', 'POST'])
def new_location():
    form = forms.Locations(flask.request.form)
    url = flask.url_for('locations.new_location')
    if flask.request.method == 'POST' and form.validate():
        query = models.Locations(
            form.location_name.data,
            form.location_position.data,
        )
        
        database.db_session.add(query)
        database.db_session.commit()
        flask.flash(flask.Markup("Successfully add new location!"), 'success')
        return flask.redirect(url)

    return flask.render_template('locations/new_location.html', form=form)


@bp.route('/locations/edit/<location_id>', methods=['GET', 'POST'])
def update_location(location_id):
    form = forms.Locations(flask.request.form)
    remove_form = forms.RemoveForm()
    query = models.Locations.by_id(location_id)
    if flask.request.method == 'POST' and form.validate():
        query.location_name = form.location_name.data
        query.location_position = form.location_position.data

        database.db_session.add(query)
        database.db_session.commit()
        flask.flash(flask.Markup("Successfully update location!"), 'success')
        return flask.render_template('locations/location.html', location=query)

    elif flask.request.method == 'POST' and remove_form.validate():
        return _remove_location(query, remove_form)

    form.location_name.data = query.location_name
    form.location_position.data = query.location_position
    
    return flask.render_template('locations/edit_location.html', form=form, remove_form=remove_form)


def _remove_location(query, remove_form):
    url = flask.url_for('locations.locations')
    action = False

    if remove_form.remove.data:
        action = True
        database.db_session.delete(query)

    if action:
        database.db_session.commit()
        flask.flash(flask.Markup('The Location Data has been successfully removed.'), 'success')

    return flask.redirect(url)