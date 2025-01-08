from sqlalchemy.orm import Session
from database import SessionLocal
from models import Species, Enclosure, Placement
import random

def populate_database():
    db: Session = SessionLocal()

    try:
        species_list = []
        for i in range(1, 1001):
            species = Species(
                name=f"Species_{i}",
                family=f"Family_{random.randint(1, 100)}",
                habitat=random.choice(["Savannah", "Forest", "Arctic", "Desert"]),
                lifespan=random.randint(5, 100)
            )
            species_list.append(species)
        db.add_all(species_list)
        db.commit()

        enclosure_list = []
        for i in range(1, 501):
            enclosure = Enclosure(
                name=f"Enclosure_{i}",
                area=random.uniform(100.0, 5000.0),
                is_indoor=random.choice([True, False]),
                has_water_source=random.choice([True, False])
            )
            enclosure_list.append(enclosure)
        db.add_all(enclosure_list)
        db.commit()

        placement_list = []
        for i in range(1, 2001):
            placement = Placement(
                species_id=random.randint(1, 1000),
                enclosure_id=random.randint(1, 500),
                animal_count=random.randint(1, 200)
            )
            placement_list.append(placement)
        db.add_all(placement_list)
        db.commit()

        print("Database populated with large dataset successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    populate_database()
