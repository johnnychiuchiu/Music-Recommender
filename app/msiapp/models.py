from msiapp import db


# Create a data model for the database to be setup for the app
class Track(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=False, nullable=False)
    artist = db.Column(db.String(100), unique=False, nullable=False)
    album = db.Column(db.String(100), unique=False, nullable=True)

    def __repr__(self):
        return '<Track %r>' % self.title
