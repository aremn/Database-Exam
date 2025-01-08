from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.database import engine
from app.models import Base
from app.routers import species, enclosures, placements

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(species.router, prefix="/species", tags=["Species"])
app.include_router(enclosures.router, prefix="/enclosures", tags=["Enclosures"])
app.include_router(placements.router, prefix="/placements", tags=["Placements"])

templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

