from typing import Tuple, Callable

from fastapi import FastAPI

from .database import Database
from .settings import read_db_config


def create_app():

    app = FastAPI()
    db = Database(read_db_config())

    @app.on_event("startup")
    def startup():
        db.setup()

    def db_callback():
        return db

    return app, db_callback
