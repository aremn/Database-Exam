from pydantic import BaseModel
from typing import Optional

class SpeciesBase(BaseModel):
    name: str
    family: str
    habitat: str
    lifespan: int

class SpeciesCreate(SpeciesBase):
    pass

class SpeciesRead(SpeciesBase):
    id: int

    class Config:
        from_attributes = True

class EnclosureBase(BaseModel):
    name: str
    is_indoor: bool
    area: float
    has_water_source: bool

class EnclosureCreate(EnclosureBase):
    pass

class EnclosureRead(EnclosureBase):
    id: int

    class Config:
        from_attributes = True

class PlacementBase(BaseModel):
    species_id: int
    enclosure_id: int
    animal_count: int

class PlacementCreate(PlacementBase):
    pass

class PlacementRead(PlacementBase):
    id: int

    class Config:
        from_attributes = True
