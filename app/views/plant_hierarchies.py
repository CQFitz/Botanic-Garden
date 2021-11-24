import flask
from app import database, forms, models


app = flask.current_app
bp = flask.Blueprint('plant_hierarchies', __name__)


@bp.route('/plant_hierarchies/')
def plant_hierarchies():
    query = models.PlantHierarchies.query.all()
    url = flask.url_for('plant_hierarchies.new_hierarchy')
    if not query:
        flask.flash(flask.Markup("It Seems to be there is nothing in the Plant Hierarchies database. Try to add something"), 'warning')
        return flask.redirect(url)

    form = None

    return flask.render_template('plants/plant_hierarchies.html', plant_hierarchies_query=query)


@bp.route('/plant_hierarchies/view/<plant_hierarchy_id>', methods=['GET', 'POST'])
def view_plant_hierarchy(plant_hierarchy_id):
    query = models.PlantHierarchies.by_id(plant_hierarchy_id)
    if not query:
        flask.abort(404)

    related_from = models.PlantHierarchies.related_from(query.parent_plant_hierarchy_id)
    related_to = models.PlantHierarchies.related_to(query.plant_hierarchy_id)
    hierarchy_category = models.PlantHierarchies.same_category(query.parent_plant_hierarchy_id)
    related_plants = models.Plants.related_hierarchy_plant(plant_hierarchy_id)

    form = None
    try: related_plants[0] 
    except IndexError: related_plants = None

    return flask.render_template('plants/plant_hierarchy.html', plant_hierarchy=query, related_from=related_from, hierarchy_category=hierarchy_category, plants=related_plants, related_to=related_to)


@bp.route('/plant_hierarchies/new', methods=['GET', 'POST'])
def new_hierarchy():
    form = forms.PlantHierarchies(flask.request.form)
    form.parent_plant_hierarchy_id.choices = [('', 'None')]+ [(g.plant_hierarchy_id, g.plant_hierarchy_name) for g in models.PlantHierarchies.query.order_by('plant_hierarchy_name')]
    url = flask.url_for('plant_hierarchies.new_hierarchy')
    if flask.request.method == 'POST' and form.validate():
        if form.parent_plant_hierarchy_id.data != '':
            query = models.PlantHierarchies(
                form.plant_hierarchy_name.data,
                form.plant_hierarchy_details.data,
                form.parent_plant_hierarchy_id.data
            )
        else:
            query = models.PlantHierarchies(
                form.plant_hierarchy_name.data,
                form.plant_hierarchy_details.data,
                None
            )
        
        database.db_session.add(query)
        database.db_session.commit()
        flask.flash(flask.Markup("Successfully add new plant hierarchy!"), 'success')
        return flask.redirect(url)

    return flask.render_template('plants/new_plant_hierarchy.html', form=form)


@bp.route('/plant_hierarchies/edit/<plant_hierarchy_id>', methods=['GET', 'POST'])
def update_hierarchy(plant_hierarchy_id):
    selected_hierarchy = 'None'
    query = models.PlantHierarchies.by_id(plant_hierarchy_id)

    related_plants = models.Plants.related_hierarchy_plant(plant_hierarchy_id)
    _parent_check = models.PlantHierarchies.parent_check(query.plant_hierarchy_id)

    form = forms.PlantHierarchies(flask.request.form)
    remove_form = forms.RemoveForm()
    url = flask.url_for('plant_hierarchies.view_plant_hierarchy', plant_hierarchy_id=query.plant_hierarchy_id)

    if not query:
        flask.abort(404)
    if query.parent_plant_hierarchy_id != None:
        selected_hierarchy = models.PlantHierarchies.by_id(query.parent_plant_hierarchy_id)
        selected_hierarchy = selected_hierarchy.plant_hierarchy_name

    form.parent_plant_hierarchy_id.choices = [(query.parent_plant_hierarchy_id, '( SELECTED ) | ' + selected_hierarchy)] + [(g.plant_hierarchy_id, g.plant_hierarchy_name) for g in models.PlantHierarchies.query.order_by('plant_hierarchy_name')]
    if flask.request.method == 'POST' and form.validate():
        query.plant_hierarchy_name = form.plant_hierarchy_name.data
        query.plant_hierarchy_details = form.plant_hierarchy_details.data
        query.parent_plant_hierarchy_id = form.parent_plant_hierarchy_id.data
        
        database.db_session.add(query)
        database.db_session.commit()
        flask.flash(flask.Markup("Successfully update plant hierarchy!"), 'success')
        return flask.redirect(url)

    elif flask.request.method == 'POST' and remove_form.validate():
        return _remove_plant_hierarchy(query, remove_form)

    form.plant_hierarchy_name.data = query.plant_hierarchy_name
    form.plant_hierarchy_details.data = query.plant_hierarchy_details
    form.parent_plant_hierarchy_id.data = query.parent_plant_hierarchy_id

    try: related_plants[0] 
    except IndexError: related_plants = None
    
    try: _parent_check[0] 
    except IndexError: _parent_check = None
    
    return flask.render_template('plants/edit_plant_hierarchy.html', form=form, remove_form=remove_form, query=query, plants=related_plants, hierarchies=_parent_check)


def _remove_plant_hierarchy(query, remove_form):
    url = flask.url_for('plant_hierarchies.plant_hierarchies')
    action = False
    _parent_check = models.PlantHierarchies.parent_check(query.plant_hierarchy_id)

    try: _parent_check[0] 
    except IndexError: _parent_check = None

    if remove_form.remove.data:
        action = True
        if _parent_check:
            for h in _parent_check:
                h.parent_plant_hierarchy_id = None
        database.db_session.delete(query)
    
    if action:
        database.db_session.commit()
        flask.flash(flask.Markup('Plant hierarchy has been successfully removed.'), 'success')
        # flask.flash(flask.Markup('Plant hierarchy has been successfully disintegrate {0}.'.format(status)), 'success')

    return flask.redirect(url)