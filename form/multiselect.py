from wtforms import Form, SelectMultipleField, SubmitField, widgets
from wtforms.validators import DataRequired
import pymysql
import pandas as pd


conn = pymysql.connect("dbmarch9.c7rrmd1b0hyo.us-west-2.rds.amazonaws.com",
                               user="usermarch9",
                               port=3306,
                               passwd="12345678",
                               db="dbmarch9")

song_df = pd.read_sql('SELECT DISTINCT song_id, title, artist_name FROM Song;', con=conn)
song_df = song_df.sort_values('artist_name', ascending=False)
data = [(song[0], song[1]+'----- '+song[2]) for index, song in song_df.iterrows()]


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