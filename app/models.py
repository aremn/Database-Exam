from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Index

Base = declarative_base()

class Species(Base):
    __tablename__ = "species"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    family = Column(String, nullable=False)
    habitat = Column(String, nullable=False)
    lifespan = Column(Integer, nullable=False)
    additional_info = Column(JSONB, nullable=True)

    placements = relationship("Placement", back_populates="species")

    __table_args__ = (
        Index("ix_species_additional_info", additional_info, postgresql_using="gin"),
    )

class Enclosure(Base):
    __tablename__ = "enclosures"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    is_indoor = Column(Boolean, nullable=False)
    area = Column(Float, nullable=False)
    has_water_source = Column(Boolean, nullable=False)

    placements = relationship("Placement", back_populates="enclosure")

class Placement(Base):
    __tablename__ = "placements"

    id = Column(Integer, primary_key=True, index=True)
    species_id = Column(Integer, ForeignKey("species.id"), nullable=False)
    enclosure_id = Column(Integer, ForeignKey("enclosures.id"), nullable=False)
    animal_count = Column(Integer, nullable=False)

    species = relationship("Species", back_populates="placements")
    enclosure = relationship("Enclosure", back_populates="placements")

