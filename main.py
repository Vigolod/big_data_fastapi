from functools import partial
from urllib.parse import quote

from fastapi import Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from urllib.parse import unquote

from starlette.staticfiles import StaticFiles

from app.app import create_app
from app.utils import get_kds_and_wr


app, db_callback = create_app()
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="stat")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request, db=Depends(db_callback)):
    vehicles_quoted = map(partial(quote, safe=""), db.vehicles)
    return templates.TemplateResponse(
        'index.html',
        {"request": request, "vehicles": zip(db.vehicles, vehicles_quoted)}
    )

@app.get("/vehicles/{vehicle}/", response_class=HTMLResponse)
async def root(request: Request, vehicle: str, db=Depends(db_callback)):
    vehicle = unquote(vehicle)
    vehicle_stats = db.get_vehicle(vehicle)
    kds, wr = get_kds_and_wr(db.columns, vehicle_stats)
    return templates.TemplateResponse(
        'vehicle.html', {"request": request, "vehicle": vehicle, "kds": kds, "wr": wr}
    )

@app.get("/extremums/", response_class=JSONResponse)
async def root(request: Request, db=Depends(db_callback)):
    result = db.get_extremum_vehicles()
    return JSONResponse(content=result)
    

