import app, logging

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:////tmp/botanic_garden_test.db')
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    logging.warning("Creating Database")
    from app.models import Base, Famillies, PlantHierarchies, Locations, Plants, PlantLocations
    logging.warning("Created database")
    Base.metadata.create_all(bind=engine)