import pandas as pd
import os
from schema import Song
from db_conn import dbConn
from schema import db
# from schema.db_models import *
import random


class ReadData():
    """
    Acquire song data from the url provided by Turi and save it into local database.
    """
    def __init__(self):
        self.SEED = 12345

    def readSongData(self):
        """
        read song data from the url provided by Turi. If the data has already exist, then read data from pickle file.

        Returns
        -------
        data.frame
            a dataframe contain the data needed for building the recommender system
        """
        if 'song.pkl' in os.listdir('../../data'):
            song_df = pd.read_pickle('../../data/song.pkl')
        else:
            # Read userid-songid-listen_count triplets
            # This step might take time to download data from external sources
            triplets_file = 'https://static.turi.com/datasets/millionsong/10000.txt'
            songs_metadata_file = 'https://static.turi.com/datasets/millionsong/song_data.csv'

            song_df_1 = pd.read_table(triplets_file, header=None)
            song_df_1.columns = ['user_id', 'song_id', 'listen_count']

            # Read song  metadata
            song_df_2 = pd.read_csv(songs_metadata_file)

            # Merge the two dataframes above to create input dataframe for recommender systems
            song_df = pd.merge(song_df_1, song_df_2.drop_duplicates(['song_id']), on="song_id", how="left")

            # Merge song title and artist_name columns to make a merged column
            song_df['song'] = song_df['title'].map(str) + " - " + song_df['artist_name']

            n_users = song_df.user_id.unique().shape[0]
            n_items = song_df.song_id.unique().shape[0]
            print(str(n_users) + ' users')
            print(str(n_items) + ' items')

            song_df.to_pickle('../data/song.pkl')

        # # keep top_n rows of the data
        # song_df = song_df.head(top)

        song_df = self.drop_freq_low(song_df)

        return(song_df)

    def drop_freq_low(self, song_df):
        """
        delete user who listen to less than 5 songs

        Parameters
        ----------
        song_df : data.frame
            data frame containing song data

        Returns
        -------
        data.frame
            a dataframe without users who listen to less than 5 songs

        """
        freq_df = song_df.groupby(['user_id']).agg({'song_id': 'count'}).reset_index(level=['user_id'])
        below_userid = freq_df[freq_df.song_id <= 5]['user_id']
        new_song_df = song_df[~song_df.user_id.isin(below_userid)]

        return(new_song_df)

    def random_select_user(self, song_df, top):

        # random sample n users from song_df
        user_list = list(song_df.user_id.unique())
        random.seed(self.SEED)
        random.shuffle(user_list)
        song_df = song_df[song_df.user_id.isin(user_list[0:top])]

        return song_df

if __name__=='__main__':
    # read song data as dataframe
    song_df = ReadData().readSongData()

    # random sample n users
    song_df = ReadData().random_select_user(song_df, 500)

    # connect to sqlite database
    conn = dbConn('../../data/song2.sqlite')

    # insert the dataframe into local database
    song_df.to_sql(name='Song', con=conn, if_exists='replace', index=True)

    # # insert the dataframe into RDS database
    # song_df.to_sql("Song", db.engine, if_exists='replace', index=False)

    print("Song Data Inserted")

    # Song.query.first()


# pd.read_sql_query("select * from " + name + ';', conn)
# pd.read_sql_query("select * from Song limit 5;", conn)


