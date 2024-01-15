from fastapi import Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.app import create_app


app, db_callback = create_app()
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request, db=Depends(db_callback)):
    vehicles_list = db.vehicles
    return templates.TemplateResponse(
        'index.html', {"request": request, "vehicles": vehicles_list}
    )
