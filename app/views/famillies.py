import flask
from app import database, forms, models


app = flask.current_app
bp = flask.Blueprint('famillies', __name__)


@bp.route('/famillies/')
def famillies():
    query = models.Famillies.query.all()
    url = flask.url_for('famillies.new_family')
    if not query:
        flask.flash(flask.Markup("It Seems to be there is nothing in the famillies database. Try to add something"), 'warning')
        return flask.redirect(url)

    form = None

    return flask.render_template('famillies/famillies.html', famillies_query=query)


@bp.route('/famillies/view/<family_id>', methods=['GET', 'POST'])
def view_family(family_id):
    query = models.Famillies.by_id(family_id)
    plants_query = models.Plants.query.filter_by(family_id=query.family_id)

    if not query:
        flask.abort(404)

    form = None

    url = flask.url_for('famillies.view_family', family_id=query.family_id)

    return flask.render_template('famillies/family.html', family=query, plants=plants_query)


@bp.route('/famillies/new', methods=['GET', 'POST'])
def new_family():
    form = forms.Famillies(flask.request.form)
    url = flask.url_for('famillies.new_family')
    if flask.request.method == 'POST' and form.validate():
        query = models.Famillies(
            form.family_name.data,
            form.family_details.data,
            form.family_description.data,
        )
        
        database.db_session.add(query)
        database.db_session.commit()
        flask.flash(flask.Markup("Successfully add new famillies!"), 'success')
        return flask.redirect(url)

    return flask.render_template('famillies/new_family.html', form=form)


@bp.route('/famillies/edit/<family_id>', methods=['GET', 'POST'])
def update_family(family_id):
    form = forms.Famillies(flask.request.form)
    related_plants = models.Plants.related_family_plant(family_id)
    remove_form = forms.RemoveForm()
    query = models.Famillies.by_id(family_id)
    url = flask.url_for('famillies.view_family', family_id=query.family_id)
    if flask.request.method == 'POST' and form.validate():
        query.family_name = form.family_name.data
        query.family_details = form.family_details.data
        query.family_description = form.family_description.data

        database.db_session.add(query)
        database.db_session.commit()
        flask.flash(flask.Markup("Successfully update family!"), 'success')
        return flask.redirect(url)

    elif flask.request.method == 'POST' and remove_form.validate():
        return _remove_family(query, remove_form)

    form.family_name.data = query.family_name
    form.family_details.data = query.family_details
    form.family_description.data = query.family_description

    try: related_plants[0] 
    except IndexError: related_plants = None
    
    return flask.render_template('famillies/edit_family.html', form=form, remove_form=remove_form, plants=related_plants, query=query)


def _remove_family(query, remove_form):
    url = flask.url_for('famillies.famillies')
    action = False

    if remove_form.remove.data:
        action = True
        database.db_session.delete(query)
    
    if action:
        database.db_session.commit()
        flask.flash(flask.Markup('The Family Data has been successfully removed.'), 'success')

    return flask.redirect(url)