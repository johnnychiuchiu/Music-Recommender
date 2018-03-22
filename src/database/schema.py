from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Final Version
class Config(object):
    """using the global variable saving in command line"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

## final version
application = Flask(__name__)
application.config.from_object(Config)
db = SQLAlchemy(application)

class Song(db.Model):
    """create a table name Song with the following schema"""
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
