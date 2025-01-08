from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Species, Placement
from app.schemas import SpeciesCreate, SpeciesRead
from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import func

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def paginated_species(request: Request, page: int = 1, db: Session = Depends(get_db)):
    limit = 10
    offset = (page - 1) * limit
    total = db.query(Species).count() 
    species_list = db.query(Species).offset(offset).limit(limit).all()  
    total_pages = (total // limit) + (1 if total % limit > 0 else 0) 

    return templates.TemplateResponse(
        "species.html",
        {
            "request": request,
            "species_list": species_list,
            "total_pages": total_pages,
            "current_page": page,
        },
    )


@router.post("/", response_model=SpeciesRead)
def create_species(species: SpeciesCreate, db: Session = Depends(get_db)):
    new_species = Species(
        name=species.name,
        family=species.family,
        habitat=species.habitat,
        lifespan=species.lifespan
    )
    db.add(new_species)
    db.commit()
    db.refresh(new_species)
    return new_species


@router.get("/", response_model=list[SpeciesRead])
def list_species(db: Session = Depends(get_db)):
    return db.query(Species).all()


@router.delete("/{species_id}", status_code=204)
def delete_species(species_id: int, db: Session = Depends(get_db)):
    species = db.query(Species).filter(Species.id == species_id).first()
    if not species:
        raise HTTPException(status_code=404, detail="Species not found")
    db.delete(species)
    db.commit()


@router.post("/add/")
async def add_species(request: Request, db: Session = Depends(get_db)):
    form_data = await request.form() 
    new_species = Species(
        name=form_data['name'],
        family=form_data['family'],
        habitat=form_data['habitat'],
        lifespan=int(form_data['lifespan']),
    )
    db.add(new_species)
    db.commit()
    return RedirectResponse(url="/species", status_code=303)

@router.get("/populate-json/")
def populate_json_field(db: Session = Depends(get_db)):
    species_list = db.query(Species).all()

    for species in species_list:
        species.additional_info = {
            "description": f"This is {species.name}, a member of the {species.family} family.",
            "conservation_status": "Least Concern",
            "region": species.habitat
        }

    db.commit()
    return {"message": "JSON fields populated"}

@router.get("/search/", response_class=HTMLResponse)
def search_species(request: Request, query: str, db: Session = Depends(get_db)):
    results = db.query(Species).filter(
        Species.additional_info["description"].astext.op("~*")(query)
    ).all()
    return templates.TemplateResponse(
        "species.html",
        {
            "request": request,
            "species_list": results,
            "current_page": 1,
            "total_pages": 1,
        },
    )


@router.get("/edit/{species_id}", response_class=HTMLResponse)
def edit_species_form(request: Request, species_id: int, db: Session = Depends(get_db)):
    species = db.query(Species).filter(Species.id == species_id).first()
    if not species:
        raise HTTPException(status_code=404, detail="Species not found")
    return templates.TemplateResponse("edit_species.html", {"request": request, "species": species})

@router.post("/edit/{species_id}")
async def edit_species(species_id: int, request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()
    species = db.query(Species).filter(Species.id == species_id).first()
    if not species:
        raise HTTPException(status_code=404, detail="Species not found")
    species.name = form_data['name']
    species.family = form_data['family']
    species.habitat = form_data['habitat']
    species.lifespan = int(form_data['lifespan'])
    db.commit()
    return RedirectResponse(url="/species", status_code=303)

@router.post("/delete/{species_id}/")
def delete_species(species_id: int, db: Session = Depends(get_db)):
    db.query(Placement).filter(Placement.species_id == species_id).delete(synchronize_session=False)

    species = db.query(Species).filter(Species.id == species_id).first()
    if not species:
        raise HTTPException(status_code=404, detail="Species not found")
    db.delete(species)
    db.commit()

    return RedirectResponse(url="/species", status_code=303)

@router.get("/filter", response_class=HTMLResponse)
def filter_species(request: Request, habitat: str = None, db: Session = Depends(get_db)):
    query = db.query(Species)
    if habitat:
        query = query.filter(Species.habitat == habitat)
    species_list = query.all()
    return templates.TemplateResponse(
        "species.html",
        {
            "request": request,
            "species_list": species_list,
            "current_page": 1, 
            "total_pages": 1,   
        }
    )


@router.get("/subquery", response_class=HTMLResponse)
def subquery_species(request: Request, db: Session = Depends(get_db)):
    subquery = db.query(
        Placement.species_id, func.sum(Placement.animal_count).label("total_animals")
    ).group_by(Placement.species_id).subquery()

    results = db.query(Species).join(
        subquery, Species.id == subquery.c.species_id
    ).filter(subquery.c.total_animals > 50).all()

    return templates.TemplateResponse(
        "species.html",
        {
            "request": request,
            "species_list": results,
            "current_page": 1,
            "total_pages": 1,
        }
    )

@router.get("/full_table", response_class=HTMLResponse)
def full_table(request: Request, db: Session = Depends(get_db)):
    results = db.query(
        Species.id.label("species_id"),
        Species.name.label("species_name"),
        Species.family,
        Species.habitat,
        Species.lifespan,
        Placement.animal_count,
        Placement.enclosure_id
    ).join(Placement, Species.id == Placement.species_id).all()

    return templates.TemplateResponse(
        "full_table.html",
        {
            "request": request,
            "results": results,
        }
    )



@router.get("/{species_id}", response_model=SpeciesRead)
def get_species(species_id: int, db: Session = Depends(get_db)):
    species = db.query(Species).filter(Species.id == species_id).first()
    if not species:
        raise HTTPException(status_code=404, detail="Species not found")
    return species

