import os

from dotenv import load_dotenv
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

app = Flask(__name__)

# sudo /opt/lampp/manager-linux-x64.run to open LAMPP

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('SQLALCHEMY_DATABASE_URI')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma=Marshmallow(app)

load_dotenv()
from app.views import views