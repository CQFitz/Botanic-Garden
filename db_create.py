import sqlalchemy

from config import app_config
from app.database import db_session
import app.models as models

FAMILLIES = [
    # ('family_name', 'family_details', 'family_description')
    # http://theplantlist.org/1.1/browse/A/ || http://theplantlist.org/1.1/browse/G/ || http://theplantlist.org/1.1/browse/P/ || http://theplantlist.org/1.1/browse/B/
    (
        'Angiosperms', 
        'Family of Flowering plants', 
        'Angiosperms are seed-bearing vascular plants. Their reproductive structures are flowers in which the ovules are enclosed in an ovary. Angiosperms are found in almost every habitat from forests and grasslands to sea margins and deserts. Angiosperms display a huge variety of life forms including trees, herbs, submerged aquatics, bulbs and epiphytes. The largest plant families are Orchids, and Compositae (daisies) and Legumes (beans). '
    ),
    (
        'Gymnosperms', 
        'Family of seed-producing plants',
        'Gymnosperms are seed-bearing vascular plants, such as cycads, ginkgo, yews and conifers, in which the ovules or seeds are not enclosed in an ovary. The word "gymnosperm" comes from the Greek word gymnospermos, meaning "naked seeds". Gymnosperm seeds develop either on the surface of scale or leaf-like appendages of cones, or at the end of short stalks.'
    ),
    (
        'Pteridophytes',
        'Family of vascular plant that disperses spores.',
        'Pteridophytes are vascular plants and have leaves (known as fronds), roots and sometimes true stems, and tree ferns have full trunks. Examples include ferns, horsetails and club-mosses. Fronds in the largest species of ferns can reach some six metres in length!'
    ),
    (
        'Bryophytes',
        'Family of herbaceous plants that grow closely packed together',
        'Bryophytes are small, non-vascular plants, such as mosses, liverworts and hornworts. They play a vital role in regulating ecosystems because they provide an important buffer system for other plants, which live alongside and benefit from the water and nutrients that bryophytes collect.'
    ),
]

PLANT_HIERARCHIES = [
    # ('plant_hierarchy_name', 'plant_hierarchy_details', 'plant_hierarchy_from_id')
    # http://theplantlist.org/1.1/browse/A/Acanthaceae/
    (
        'Acanthaceae',
        'The family Acanthaceae is in the major group Angiosperms (Flowering plants).',
        '',
    ),
    (
        'Acanthodium',
        'The genus Acanthodium is in the family Acanthaceae in the major group Angiosperms (Flowering plants).',
        '1',
    ),
    (
        'Acanthopale',
        'The genus Acanthopale is in the family Acanthaceae in the major group Angiosperms (Flowering plants).',
        '1'
    ),
    (
        'Acanthopale aethiogermanica Ensermu',
        'The genus Acanthopale is in the family Acanthaceae in the major group Angiosperms (Flowering plants).',
        '3'
    ),
    (
        'Acanthopale albosetulosa C.B.Clarke'
        'The genus Acanthopale is in the family Acanthaceae in the major group Angiosperms (Flowering plants).',
        '3'
    ),
    (
        'Acanthopsis',
        'The genus Acanthopsis is in the family Acanthaceae in the major group Angiosperms (Flowering plants).',
        '1'
    ),
    (
        'Acanthopsis carduifolia (L.f.) Schinz',
        'The genus Acanthopsis is in the family Acanthaceae in the major group Angiosperms (Flowering plants).',
        '6'
    )
]

PLANTS = [
    # ('plant_details', 'plant_hierachy_id', 'family_id')
    # http://theplantlist.org/1.1/browse/A/Acanthaceae/Acanthopale/
    # https://www.zimbabweflora.co.zw/speciesdata/species.php?species_id=153370
    (
        'Erect or somewhat scrambling Shrub-like perennial herb, up to 2.5 m tall. Leaves opposite, largest 8-24 cm long, ovate to elliptic with a distinct drip-tip, dark green, hairy on both surfaces; petiole 2-6.5 cm long. Flowers in more or less condensed terminal racemose heads, white with purple-pink markings, softly hairy on the outside of the corolla. Capsule 11-14 mm long.',
        '3',
        '1',
    ),
    (
        'Acanthopale albosetulosa C.B.Clarke',
        '3',
        '1',
    )
]

LOCATIONS = [
    # ('location_name', 'location_position')
    # https://eol.org/media/10550829
    (
        'Nhandore Peak, Mt Gorongosa, Mozambique Habitat',
        'In the understorey of evergreen forest, often in large numbers.',
    ),
]

PLANT_LOCATIONS = [
    # ('plant_id', 'location_id')
    (
        '1',
        '1'
    ),
    (
        '2',
        '1'
    )
]

def add_famillies(famillies, main_class):
    for name, details, description in famillies:
        family = main_class(name, details, description)
        db_session.add(family)


def add_plant_hierarchies(plant_hierarhies, main_class):
    for name, details, hierarchy_from in plant_hierarchies:
        plant_hierarchy = main_class(name, details, hierarchy_from)
        db_session.add(plant_hierarchy)


def add_locations(locations, main_class):
    for name, position in locations:
        location = main_class(name, position)
        db_session.add(location)


def add_plants(plants, main_class):
    for details, family, hierarchy in plants:
        plant = main_class(details, family, hierarchy)
        db_session.add(plant)


def init_db():
    print("Creating Database...")
    from app.models import Base, Famillies, PlantHierarchies, Locations, Plants, PlantLocations
    print("Created database.")
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    database_empty = False
    # Test for the any table, assume database is empty if it's not created
    try:
        models.Famillies.query.first()
    except (sqlalchemy.exc.ProgrammingError, sqlalchemy.exc.OperationalError):
        database_empty = True

    print("Creating all tables...")
    init_db()

    famillies_test = models.Famillies.query.first()
    if not famillies_test:
        print("Adding famillies...")
        add_famillies(FAMILLIES, models.Famillies)

    plant_hierarchy_test = models.PlantHierarchies.query.first()
    if not plant_hierarchy_test:
        print("Adding plant hierarchies...")
        add_plant_hierarchies(PLANT_HIERARCHIES, models.PlantHierarchies)

    plant_test = models.Plants.query.first()
    if not plant_test:
        print("Adding plants...")
        add_plants(PLANTS, models.Plants)

    location_test = models.Locations.query.first()
    if not location_test:
        print("Adding location...")
        add_locations(LOCATIONS, models.Locations)

    db.session.commit()

    if database_empty:
        print("database empty")