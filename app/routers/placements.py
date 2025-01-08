from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Placement, Species, Enclosure
from app.schemas import PlacementCreate, PlacementRead
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
def paginated_placements(request: Request, page: int = 1, db: Session = Depends(get_db)):
    limit = 20
    offset = (page - 1) * limit
    total = db.query(Placement).count()
    placements_list = db.query(Placement).offset(offset).limit(limit).all()
    total_pages = (total // limit) + (1 if total % limit > 0 else 0)

    return templates.TemplateResponse(
        "placements.html",
        {
            "request": request,
            "placements_list": placements_list,
            "total_pages": total_pages,
            "current_page": page,
        },
    )

@router.post("/", response_model=PlacementRead)
def create_placement(placement: PlacementCreate, db: Session = Depends(get_db)):
    new_placement = Placement(
        species_id=placement.species_id,
        enclosure_id=placement.enclosure_id,
        animal_count=placement.animal_count
    )
    db.add(new_placement)
    db.commit()
    db.refresh(new_placement)
    return new_placement

@router.get("/{placement_id}", response_model=PlacementRead)
def get_placement(placement_id: int, db: Session = Depends(get_db)):
    placement = db.query(Placement).filter(Placement.id == placement_id).first()
    if not placement:
        raise HTTPException(status_code=404, detail="Placement not found")
    return placement

@router.get("/", response_model=list[PlacementRead])
def list_placements(db: Session = Depends(get_db)):
    return db.query(Placement).all()

@router.post("/add/")
async def add_placement(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    new_placement = Placement(
        species_id=int(form['species_id']),
        enclosure_id=int(form['enclosure_id']),
        animal_count=int(form['animal_count'])
    )
    db.add(new_placement)
    db.commit()
    return HTMLResponse(status_code=303, headers={"Location": "/placements"})

@router.get("/edit/{placement_id}", response_class=HTMLResponse)
def edit_placement_form(request: Request, placement_id: int, db: Session = Depends(get_db)):
    placement = db.query(Placement).filter(Placement.id == placement_id).first()
    if not placement:
        raise HTTPException(status_code=404, detail="Placement not found")
    return templates.TemplateResponse("edit_placement.html", {"request": request, "placement": placement})

@router.post("/edit/{placement_id}")
async def edit_placement(placement_id: int, request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    placement = db.query(Placement).filter(Placement.id == placement_id).first()
    if not placement:
        raise HTTPException(status_code=404, detail="Placement not found")
    placement.species_id = int(form['species_id'])
    placement.enclosure_id = int(form['enclosure_id'])
    placement.animal_count = int(form['animal_count'])
    db.commit()
    return HTMLResponse(status_code=303, headers={"Location": "/placements"})

@router.post("/delete/{placement_id}/")
def delete_placement(placement_id: int, db: Session = Depends(get_db)):
    placement = db.query(Placement).filter(Placement.id == placement_id).first()
    if not placement:
        raise HTTPException(status_code=404, detail="Placement not found")
    db.delete(placement)
    db.commit()
    return HTMLResponse(status_code=303, headers={"Location": "/placements"})

@router.get("/filter", response_class=HTMLResponse)
def filter_placements(request: Request, species_name: str = None, db: Session = Depends(get_db)):
    query = db.query(Placement, Species, Enclosure).join(Species).join(Enclosure)
    if species_name:
        query = query.filter(Species.name.ilike(f"%{species_name}%"))
    placements_list = query.all()
    return templates.TemplateResponse(
        "placements.html",
        {"request": request, "placements_list": placements_list, "species_name": species_name}
    )

