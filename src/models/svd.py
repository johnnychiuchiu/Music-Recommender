import pandas as pd
from surprise import Dataset
from surprise import Reader
from surprise import SVD
from collections import defaultdict
import os
import sqlite3
import random

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import pymysql
from config import Config

class mySVD():
    """
    Build a recommender system using Singular Value Decomposition Method
    """
    def __init__(self, top):
        self.DEFAULT_COUNT = 50
        self.SEED = 12345
        self.song_df = self.readSongData(top)
        pass

    def readSongData(self, top):
        """
        Read song data from database

        Parameters
        ----------
        top : int
            random sample n users from song_df

        Return
        -------
        data.frame
            a pandas dataframe with columns 'user_id', 'song_id', 'listen_count', 'title', 'release', 'artist_name', 'year', 'song'

        """

        # # Read from local sqlite database
        # path = os.getcwd() + '/data/song.sqlite' #/data/song.sqlite /../..
        # print(path)
        # song_df = pd.read_sql_query("SELECT * FROM Song;", conn)

        # # Read data from RDS
        # app = Flask(__name__)
        # app.config.from_object('config')
        # db = SQLAlchemy(app)
        # song_df = pd.read_sql("SELECT * FROM songs;", db.engine)

        # Try pymysql to read data from RDS


        conn = pymysql.connect(Config.host, user=Config.user, port=Config.port,
                               passwd=Config.password, db=Config.dbname)

        song_df = pd.read_sql('SELECT * FROM songs;', con=conn)

        # random sample n users from song_df
        user_list = list(song_df.user_id.unique())
        random.seed(self.SEED)
        random.shuffle(user_list)
        song_df = song_df[song_df.user_id.isin(user_list[0:top])]

        return song_df

    def createNewObs(self, songidList):
        """
        Append a new row with userId Johnny that is interested in some selected songs

        Parameters
        ----------
        songidList : list
            the user selected song_ids with format like `SOAKIMP12A8C130995`

        Returns
        -------
        data.frame
            a pandas dataframe with columns 'user_id', 'song_id', 'listen_count'

        """

        ratings_dict = {'user_id': ['johnny']*len(songidList),
                        'song_id': songidList,
                        'listen_count': [self.DEFAULT_COUNT]*len(songidList)}
        newObs = pd.DataFrame(ratings_dict)
        newObs = newObs[['user_id', 'song_id', 'listen_count']]

        return newObs

    def readSurpriseFormat(self, newObs):
        """
        combine newObs dataframe with song dataframe and transform it into Surprise data format

        Parameters
        ----------
        newObs : data.frame
            the dataframe obtain from the function createNewObs
        top : int
            filter the top n rows from the input song dataframe, this parameter will be passing into the function readSongData

        Returns
        -------
        surprise.dataset

        """

        # A reader is still needed but only the rating_scale param is requiered.
        reader = Reader(rating_scale=(1, 100))

        # get train data
        train = self.song_df[['user_id', 'song_id', 'listen_count']]

        # combine together
        full = pd.concat([train, newObs]).reset_index(drop=True)

        # The columns must correspond to user id, item id and ratings (in that order).
        data = Dataset.load_from_df(full, reader)

        return data

    def fitModel(self, data):
        """
        train a recommender system using SVD with pre-defined parameters

        Parameters
        ----------
        data : surprise.dataset
            a surprise.dataset object obtained from the function readSurpriseFormat

        Returns
        -------
        data.frame
            A recommended list of songs for the application user

        """

        # fit model
        trainset = data.build_full_trainset()
        algo_svd = SVD(n_factors=50, lr_all=0.002, reg_all=0.04, random_state=12345) # parameters tuned using 2000 user_id
        algo_svd.fit(trainset)

        # predict all the cells without values
        testset = trainset.build_anti_testset()
        predictions_svd = algo_svd.test(testset)

        # get the top n recommendations for the user of the app. I name it Johnny.
        # a list contains tuples of ('song_id', 'score'), sorted by score
        top_n_svd = self.get_top_n(predictions_svd, n=10)
        top_list = top_n_svd['johnny']

        # get the recommended playlist
        user_recommend = self.getSongData(top_list)

        return user_recommend

    def getSongData(self, top_list):
        """
        Match the top n song_id back to song_df to get the complete song information

        Parameters
        ----------
        top_list : list
            a list contains tuples of ('song_id', 'score'), sorted by score

        Returns
        -------
        data.frame
            A dataframe containing the songs in the top_list, sorted by score.
        """

        user_score = pd.DataFrame(top_list).rename(columns={0: 'song_id', 1: 'score'})
        user_recommend = pd.merge(user_score,
                                  self.song_df[['song_id', 'title', 'release', 'artist_name', 'song']].drop_duplicates(),
                                  on='song_id', how='left')
        return user_recommend

    def get_top_n(self, predictions, n=10):
        """
        Return the top-N recommendation for each user from a set of predictions.

        Parameters
        ----------
        predictions :
            The list of predictions, as returned by the test method of an algorithm.
        n : int
            The number of recommendation to output for each user. Default is 10.

        Returns
        -------
        dict
            A dict where keys are user (raw) ids and values are lists of tuples: [(raw item id, rating estimation), ...] of size n.
        """

        # First map the predictions to each user.
        top_n = defaultdict(list)
        for uid, iid, true_r, est, _ in predictions:
            top_n[uid].append((iid, est))

        # Then sort the predictions for each user and retrieve the k highest ones.
        for uid, user_ratings in top_n.items():
            user_ratings.sort(key=lambda x: x[1], reverse=True)
            top_n[uid] = user_ratings[:n]

        return top_n

if __name__=='__main__':
    svd = mySVD(top=100)
    newObs = svd.createNewObs(['SOAKIMP12A8C130995','SOBBMDR12A8C13253B','SOBXHDL12A81C204C0','SOBYHAJ12A6701BF1D','SODACBL12A8C13C273'])
    data = svd.readSurpriseFormat(newObs)
    user_recommend = svd.fitModel(data)



