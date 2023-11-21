from sqlalchemy.orm import DeclarativeBase
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_migrate import Migrate


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
# create the app
app = Flask(__name__, template_folder='templates')
migrate = Migrate(app, db, render_as_batch=True)

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# initialize the app with the extension

# db.init_app(app)
# migrate.init_app(app, db)


def create_app():
    db.init_app(app)
    migrate.init_app(app, db)
    print("creating database in config...")
