from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from src.database.config import Config
import os

# Set db path
db_path = '../../data/song2.sqlite'

# local version
# initialized flask app
app = Flask(__name__)

# SQLAlchemy configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Initialize the database
db = SQLAlchemy(app)

## EB version
# # initialized flask app
# application = Flask(__name__)
#
# # application = Flask(__name__)
# application.config.from_object('config')
#
# db = SQLAlchemy(application)

# # Final Version
# class Config(object):
#    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-key'
#    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
#    SQLALCHEMY_TRACK_MODIFICATIONS = False
#
# ## Logan's version
# application = Flask(__name__)
# application.config.from_object(Config)
# db = SQLAlchemy(application)

class Song(db.Model):
    """
    create a table name Song with the following schema
    """
    __tablename__ = 'Song'

    index = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(80), nullable=False)
    song_id = db.Column(db.String(80), nullable=False)
    listen_count = db.Column(db.Integer)
    title = db.Column(db.String(80), nullable=False)
    release = db.Column(db.String(80), nullable=False)
    artist_name = db.Column(db.String(80), nullable=False)
    year = db.Column(db.Integer)
    song = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.user_id
