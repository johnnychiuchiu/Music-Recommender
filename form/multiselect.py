from wtforms import Form, SelectMultipleField, SubmitField, widgets
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
import sqlite3
import os
import pymysql
import pandas as pd

# connect to db to get unique song, singer

path = os.getcwd()+'/data/song2.sqlite' #/..
conn = sqlite3.connect(path)
cursor = conn.execute('SELECT DISTINCT song_id, title, artist_name FROM Song;')
song_df=pd.DataFrame(cursor.fetchall())
song_df.columns=['song_id', 'title', 'artist_name']
song_df = song_df.sort_values('artist_name', ascending=False)
data = [(song[0], song[1]+'----- '+song[2]) for index, song in song_df.iterrows()]
# data = [(song[0], song[1]+'----- '+song[2]) for i, song in enumerate(cursor.fetchall())]

# import sys
# import pandas as pd
# sys.path.append('../src/database')
# from src.database.schema import db
# song_df = pd.read_sql("SELECT * FROM Song;", db.engine)

# # current version
# conn = pymysql.connect(os.environ.get('HOST'), user=os.environ.get('USER'), port=int(os.environ.get('PORT')),
#                        passwd=os.environ.get('PASSWORD'), db=os.environ.get('DBNAME'))

# # try tutorial version
# conn = pymysql.connect(os.environ['HOST'], user=os.environ['USER'], port=int(os.environ['PORT']),
#                        passwd=os.environ['PASSWORD'], db=os.environ['DBNAME'])

# # Final Version
# conn = pymysql.connect("aag31r5zpl942v.c7rrmd1b0hyo.us-west-2.rds.amazonaws.com",
#                                user="ebusermarch02",
#                                port=3306,
#                                passwd="12345678",
#                                db="ebdb")

# song_df = pd.read_sql('SELECT DISTINCT song_id, title, artist_name FROM Song;', con=conn)
# data = [(song[0], song[1]+'----- '+song[2]) for index, song in song_df.iterrows()]
# cursor = conn.execute('SELECT DISTINCT artist_name FROM Song limit 100;')
# data = [(str(i), artist[0]) for i, artist in enumerate(cursor.fetchall())]


class ArtistForm(Form):
    artist = SelectMultipleField(
        u'Pick Things!',
        choices=data,
        option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False),
        validators = [DataRequired()]
        )

if __name__=='__main__':
    print(data)