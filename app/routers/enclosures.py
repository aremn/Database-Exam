from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Enclosure, Placement
from app.schemas import EnclosureCreate, EnclosureRead
from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import func, asc, desc

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def get_enclosures(
    request: Request,
    page: int = 1,
    sort_by: str = "name",
    order: str = "asc",
    db: Session = Depends(get_db),
):
    limit = 10
    offset = (page - 1) * limit

    valid_sort_fields = ["name", "area", "is_indoor", "has_water_source"]
    if sort_by not in valid_sort_fields:
        sort_by = "name"

    order_func = desc if order.lower() == "desc" else asc

    enclosures = (
        db.query(Enclosure)
        .order_by(order_func(getattr(Enclosure, sort_by)))
        .offset(offset)
        .limit(limit)
        .all()
    )

    total = db.query(Enclosure).count()
    total_pages = (total // limit) + (1 if total % limit > 0 else 0)

    return templates.TemplateResponse(
        "enclosures.html",
        {
            "request": request,
            "enclosures_list": enclosures,
            "total_pages": total_pages,
            "current_page": page,
            "sort_by": sort_by,
            "order": order,
        },
    )


@router.post("/", response_model=EnclosureRead)
def create_enclosure(enclosure: EnclosureCreate, db: Session = Depends(get_db)):
    new_enclosure = Enclosure(
        name=enclosure.name,
        is_indoor=enclosure.is_indoor,
        area=enclosure.area,
        has_water_source=enclosure.has_water_source,
    )
    db.add(new_enclosure)
    db.commit()
    db.refresh(new_enclosure)
    return new_enclosure


@router.post("/add/")
async def add_enclosure(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    new_enclosure = Enclosure(
        name=form["name"],
        is_indoor="is_indoor" in form,
        area=float(form["area"]),
        has_water_source="has_water_source" in form,
    )
    db.add(new_enclosure)
    db.commit()
    return HTMLResponse(status_code=303, headers={"Location": "/enclosures"})


@router.get("/edit/{enclosure_id}", response_class=HTMLResponse)
def edit_enclosure_form(request: Request, enclosure_id: int, db: Session = Depends(get_db)):
    enclosure = db.query(Enclosure).filter(Enclosure.id == enclosure_id).first()
    if not enclosure:
        raise HTTPException(status_code=404, detail="Enclosure not found")
    return templates.TemplateResponse("edit_enclosures.html", {"request": request, "enclosure": enclosure})


@router.post("/edit/{enclosure_id}")
async def edit_enclosure(enclosure_id: int, request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    enclosure = db.query(Enclosure).filter(Enclosure.id == enclosure_id).first()
    if not enclosure:
        raise HTTPException(status_code=404, detail="Enclosure not found")
    enclosure.name = form["name"]
    enclosure.area = float(form["area"])
    enclosure.is_indoor = "is_indoor" in form
    enclosure.has_water_source = "has_water_source" in form
    db.commit()
    return HTMLResponse(status_code=303, headers={"Location": "/enclosures"})


@router.post("/delete/{enclosure_id}/")
def delete_enclosure(enclosure_id: int, db: Session = Depends(get_db)):
    db.query(Placement).filter(Placement.enclosure_id == enclosure_id).delete(synchronize_session=False)

    enclosure = db.query(Enclosure).filter(Enclosure.id == enclosure_id).first()
    if not enclosure:
        raise HTTPException(status_code=404, detail="Enclosure not found")
    db.delete(enclosure)
    db.commit()

    return RedirectResponse(url="/enclosures", status_code=303)


@router.post("/update-area/")
def update_enclosure_area(db: Session = Depends(get_db)):
    updated_rows = db.query(Enclosure).filter(Enclosure.is_indoor == True).update(
        {Enclosure.area: Enclosure.area * 1.1}, synchronize_session=False
    )
    db.commit()
    return {"message": f"{updated_rows} indoor enclosures updated"}


@router.get("/group-by", response_class=HTMLResponse)
def group_by_enclosures(request: Request, db: Session = Depends(get_db)):
    results = db.query(
        Enclosure.name, func.count(Placement.id).label("species_count")
    ).join(Placement).group_by(Enclosure.name).all()
    return templates.TemplateResponse(
        "enclosures_group.html",
        {"request": request, "results": results},
    )
