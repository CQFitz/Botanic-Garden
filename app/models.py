# app/models.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from app.database import db_session

Base = declarative_base()


class Famillies(Base):
    """
    Create Famillies table
    """

    __tablename__ = 'famillies'
    query = db_session.query_property()


    family_id = Column(Integer, primary_key=True)
    family_name = Column(String(60), index=True)
    family_details = Column(String(60))
    family_description = Column(String(200))
    # plant = relationship("Plants") # Keluarkan Ralat sahaja lah
    plant = relationship("Plants", back_populates="family", cascade='all, delete-orphan')

    def __init__(self, name, details, description):
        self.family_name = name
        self.family_details = details
        self.family_description = description

    def __repr__(self):
        return '<{0} #fid{1.family_id} #fin{1.family_name} #fds{1.family_details} #fd{1.family_description}>'.format(type(self).__name__, self)

    @classmethod
    def by_id(cls, family_id):
        family = cls.query.filter_by(family_id=family_id).first()
        return family


class PlantHierarchies(Base):
    """
    Create Plant Hierarchies table
    """

    __tablename__ = 'plant_hierarchies'
    query = db_session.query_property()

    plant_hierarchy_id = Column(Integer, primary_key=True)
    parent_plant_hierarchy_id = Column(Integer, ForeignKey('plant_hierarchies.plant_hierarchy_id'), index=True, default=None)
    plant_hierarchy_name = Column(String(60), index=True)
    plant_hierarchy_details = Column(String(200))
    plant = relationship("Plants", back_populates="plant_hierarchy", cascade='all, delete-orphan')

    def __init__(self, name=None, details=None, hierarchy_from=None):
        self.plant_hierarchy_name = name
        self.plant_hierarchy_details = details
        self.parent_plant_hierarchy_id = hierarchy_from


    def __repr__(self):
        return '<{0} #phid{1.plant_hierarchy_id} #pphid{1.parent_plant_hierarchy_id} #phn{1.plant_hierarchy_name} #phds{1.plant_hierarchy_details}>'.format(type(self).__name__, self)

    @classmethod
    def by_id(cls, plant_hierarchy_id):
        plant_hierarchy = cls.query.filter_by(plant_hierarchy_id=plant_hierarchy_id).first()
        return plant_hierarchy

    @classmethod
    def parent_check(cls, plant_hierarchy_id):
        parent_hierarchy = cls.query.filter_by(parent_plant_hierarchy_id=plant_hierarchy_id)
        return parent_hierarchy

    @classmethod
    def related_from(cls, parent_plant_hierarchy_id):
        related_info = cls.query.filter_by(plant_hierarchy_id=parent_plant_hierarchy_id).first()
        return related_info

    @classmethod
    def related_to(cls, plant_hierarchy_id):
        related_info = cls.query.filter_by(parent_plant_hierarchy_id=plant_hierarchy_id)
        return related_info

    @classmethod
    def same_category(cls, parent_plant_hierarchy_id):
        hierarchy_category = cls.query.filter_by(parent_plant_hierarchy_id=parent_plant_hierarchy_id)
        return hierarchy_category



class Plants(Base):
    """
    Create a Plants table
    """

    __tablename__ = 'plants'
    query = db_session.query_property()

    plant_id = Column(Integer, primary_key=True)
    plant_hierarchy_id = Column(Integer, ForeignKey('plant_hierarchies.plant_hierarchy_id'), nullable=False)
    family_id = Column(Integer, ForeignKey('famillies.family_id'), nullable=False)
    plant_details = Column(String(100), nullable=False)
    plant_hierarchy = relationship("PlantHierarchies", back_populates="plant")
    family = relationship("Famillies", back_populates="plant")
    plant_location = relationship("PlantLocations", back_populates="plant", cascade='all, delete-orphan')
    
    def __init__(self, plant_hierarchy_id, family_id, details):
        self.plant_hierarchy_id = plant_hierarchy_id
        self.family_id = family_id
        self.plant_details = details

    def __repr__(self):
        return '<{0} #phid{1.plant_hierarchy_id} #fid{1.family_id} #pds{1.plant_details}>'.format(type(self).__name__, self)

    @classmethod
    def by_id(cls, plant_id):
        plant = cls.query.filter_by(plant_id=plant_id).first()
        return plant

    @classmethod
    def related_family_plant(cls, family_id):
        same_family_plant = cls.query.filter_by(family_id=family_id)
        return same_family_plant

    @classmethod
    def related_hierarchy_plant(cls, plant_hierarchy_id):
        same_hierarchy_plant = cls.query.filter_by(plant_hierarchy_id=plant_hierarchy_id)
        return same_hierarchy_plant


class Locations(Base):
    """
    Create a Locations table
    """

    __tablename__ = 'locations'
    query = db_session.query_property()


    location_id = Column(Integer, primary_key=True)
    location_name = Column(String(60), index=True)
    # posisi lokasi, macam dekat baris mana, letak kat bahagian mana...
    location_position = Column(String(100))
    plant_location = relationship("PlantLocations")

    def __init__(self, name, posisi):
        self.location_name = name
        self.location_position = posisi

    def __repr__(self):
        return '<{0} #lid{1.location_id} #ln{1.location_name} #lp{1.location_position}>'.format(type(self).__name__, self)

    @classmethod
    def by_id(cls, location_id):
        location = cls.query.filter_by(location_id=location_id).first()
        return location


class PlantLocations(Base):
    """
    Create Plant Locations Table
    """

    __tablename__ = 'plants_locations'
    query = db_session.query_property()


    plant_id = Column(Integer, ForeignKey('plants.plant_id'), primary_key=True, nullable=False)
    plant_location_id = Column(Integer, ForeignKey('locations.location_id'), primary_key=True, nullable=False)
    plant = relationship("Plants", back_populates="plant_location")
    location = relationship("Locations", back_populates='plant_location')


    def __init__(self, plant_id, location_id):
        self.plant_id = plant_id
        self.plant_location_id = location_id


    def __repr__(self):
        return '<{0} #pid{1.plant_id} #lid{1.plant_location_id}>'.format(type(self).__name__, self)

    # Get Location
    @classmethod
    def by_plant_id(cls, plant_id):
        plant_location = db_session.query(PlantLocations).filter_by(plant_id=plant_id).first()
        try:
            location = db_session.query(Locations).join(PlantLocations.location).filter_by(location_id=plant_location.plant_location_id).first()
        except: 
            location = None
        return location


    @classmethod
    def by_location_id(cls, location_id):
        location = cls.query(Locations).join(PlantLocations.plant_location).filter_by(location_id=location_id)
        return location