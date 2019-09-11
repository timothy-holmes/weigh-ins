from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)
app._static_folder
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

from app import routes, models

if __name__ == "__main__":
    app.run()
