from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv('../.env.local')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQL_CON']
db = SQLAlchemy(app)

from condoparser.jpa import Source, Status, Offer, Condo
