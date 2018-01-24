from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# SQLAlchemy configuration (can update with AWS RDS settings)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/tracks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Initialize the database
db = SQLAlchemy(app)