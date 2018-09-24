from app import app
from db import db

db.init_app(app)


@app.before_first_request
def create_tables():  # create db with tables before first request
    db.create_all()