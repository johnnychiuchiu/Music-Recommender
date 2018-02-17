from wtforms import widgets
from wtforms import Form, SelectMultipleField, SubmitField
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
import sqlite3
import os

# connect to db to get unique song, singer

path = os.getcwd()+'/data/song.sqlite'
conn = sqlite3.connect(path)
cursor = conn.execute('SELECT DISTINCT title, artist_name FROM Song limit 100;')
data = [(i, song[0]+'----- '+song[1]) for i, song in enumerate(cursor.fetchall())]

class ExampleForm(Form):
    example = SelectMultipleField(
        'Pick Things!',
        choices=data,
        option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False),
        validators = [DataRequired()]
        )
    submit = SubmitField('Get Playlist!')

class backForm(Form):
    submit = SubmitField('Back')

if __name__=='__main__':
    print(data)