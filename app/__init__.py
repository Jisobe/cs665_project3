from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine
import sqlite3

db = SQLAlchemy()

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

def create_app():
    app=Flask(__name__, instance_relative_config=True)
    app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///health.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

    db.init_app(app)

    from .blueprints.patients import patients_bp

    app.register_blueprint(patients_bp, url_prefix="/patients")

    with app.app_context():
        from . import models
        db.create_all()

    return app
