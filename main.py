from typing import Annotated

from fastapi import FastAPI, APIRouter, Depends, Request, HTTPException
from flask import redirect
from requests import Session
from starlette.responses import RedirectResponse
from routes.aid import router as aid_router
from fastapi.staticfiles import StaticFiles
from database.settings import engine, SessionLocal
from database.models import Base, Person
from fastapi.templating import Jinja2Templates

Base.metadata.create_all(bind=engine)

# Running App
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(aid_router)


def connect():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(connect)]


# Pages
@app.get("/")
async def root(request: Request, db: db_dependency):

    try:
        all_result = db.query(Person).all()
        processing_result = db.query(Person).filter(Person.status == "PROCESSING").all()
        high = db.query(Person).filter(Person.score >= 70).all()
        medium = db.query(Person).filter(Person.score >= 30).filter(Person.score < 70).all()
        low = db.query(Person).filter(Person.score < 30).all()

        return templates.TemplateResponse("home.html", {"processing_result" : processing_result, "all_result" : all_result, "request" : request, "high" : high, "medium" : medium, "low" : low})



    except Exception as e:
        raise HTTPException(status_code=500, detail="Error processing the request")

@app.get("/map")
async def Map(request: Request):
    return templates.TemplateResponse("map.html", {"request": request})

@app.get("/find-area")
async def find_area(request: Request):
    return templates.TemplateResponse("find_area.html", {"request": request})