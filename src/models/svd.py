import pandas as pd
from surprise import Dataset
from surprise import Reader
from surprise import SVD, KNNWithMeans
from collections import defaultdict
import os
import sqlite3
import random
# sys.path.append('../database')
# from src.database.schema import db, application

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import pymysql
# from src.models.config import Config

class mySVD():
    """
    Build a recommender system using Singular Value Decomposition Method
    """
    def __init__(self):
        self.DEFAULT_COUNT = 50
        self.SEED = 12345
        self.song_df = self.readSongData()
        self.songidList = list(self.song_df['song_id'].unique())
        pass

    def readSongData(self):
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
        # path = os.getcwd() + '/data/song2.sqlite' #/data/song.sqlite /../..
        # print(path)
        # conn = sqlite3.connect(path)
        # song_df = pd.read_sql_query("SELECT * FROM Song;", conn)

        # Read data from RDS
        # app = Flask(__name__)
        # app.config.from_object('config')
        # db = SQLAlchemy(app)
        # db.init_app(application)
        # song_df = pd.read_sql("SELECT * FROM Song;", db.engine)

        # # Try pymysql to read data from RDS
        # conn = pymysql.connect(os.environ.get('HOST'), user=os.environ.get('USER'), port=int(os.environ.get('PORT')),
        #                        passwd=os.environ.get('PASSWORD'), db=os.environ.get('DBNAME'))

        # # try tutorial version
        # conn = pymysql.connect(os.environ['HOST'], user=os.environ['USER'], port=int(os.environ['PORT']),
        #                        passwd=os.environ['PASSWORD'], db=os.environ['DBNAME'])

        # try just using real host and everything
        conn = pymysql.connect("dbmarch9.c7rrmd1b0hyo.us-west-2.rds.amazonaws.com",
                               user="usermarch9",
                               port=3306,
                               passwd="12345678",
                               db="dbmarch9")

        song_df = pd.read_sql('SELECT * FROM Song;', con=conn)

        # # random sample n users from song_df
        # user_list = list(song_df.user_id.unique())
        # random.seed(self.SEED)
        # random.shuffle(user_list)
        # song_df = song_df[song_df.user_id.isin(user_list[0:top])]

        return song_df

    def trainGenerator(self, song_df, newObs):


        train = song_df[['user_id', 'song_id', 'listen_count']]

        # A reader is still needed but only the rating_scale param is requiered.
        # reader = Reader(line_format='user_id song_id listen_count', rating_scale=(1, 100))
        reader = Reader(line_format='user item rating', rating_scale=(1, 100))
        trainset_load = Dataset.load_from_df(pd.concat([train,newObs]), reader)
        trainset = trainset_load.build_full_trainset()
        return trainset

    def testGenerator(self, df):

        return [(uid, iid, r) for (uid, iid, r) in zip(df['user_id'], df['song_id'], df['listen_count'])]

    def createNewObs(self, targetSongidList):
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

        newObs = pd.DataFrame({'user_id': ['johnny'] * len(self.songidList),
                                'song_id': self.songidList,
                                'listen_count': 0})[['user_id', 'song_id', 'listen_count']]

        mask = newObs['song_id'].isin(targetSongidList)
        column_name = 'listen_count'
        newObs.loc[mask, column_name] = self.DEFAULT_COUNT

        # ratings_dict = {'user_id': ['johnny']*len(songidList),
        #                 'song_id': songidList,
        #                 'listen_count': [self.DEFAULT_COUNT]*len(songidList)}
        # newObs = pd.DataFrame(ratings_dict)
        # newObs = newObs[['user_id', 'song_id', 'listen_count']]

        return newObs

    # def readSurpriseFormat(self, newObs):
    #     """
    #     combine newObs dataframe with song dataframe and transform it into Surprise data format
    #
    #     Parameters
    #     ----------
    #     newObs : data.frame
    #         the dataframe obtain from the function createNewObs
    #     top : int
    #         filter the top n rows from the input song dataframe, this parameter will be passing into the function readSongData
    #
    #     Returns
    #     -------
    #     surprise.dataset
    #
    #     """
    #
    #     # A reader is still needed but only the rating_scale param is requiered.
    #     reader = Reader(rating_scale=(1, 100))
    #
    #     # get train data
    #     train = self.song_df[['user_id', 'song_id', 'listen_count']]
    #
    #     # combine together
    #     full = pd.concat([train, newObs]).reset_index(drop=True)
    #
    #     # The columns must correspond to user id, item id and ratings (in that order).
    #     data = Dataset.load_from_df(full, reader)
    #
    #     return data

    def fitModel(self, trainset):
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
        algo_svd = SVD(n_factors=50, lr_all=0.002, reg_all=0.04, random_state=12345) # parameters tuned using 2000 user_id
        algo_svd.fit(trainset)

        return algo_svd

        # # predict all the cells without values
        # testset = trainset.build_anti_testset()
        # predictions_svd = algo_svd.test(testset)
        #
        # # get the top n recommendations for the user of the app. I name it Johnny.
        # # a list contains tuples of ('song_id', 'score'), sorted by score
        # top_n_svd = self.get_top_n(predictions_svd, n=10)
        # top_list = top_n_svd['johnny']
        #
        # # get the recommended playlist
        # user_recommend = self.getSongData(top_list)
        #
        # return user_recommend

    def predictTopSong(self, algo_svd, testset, targetSongidList):


        # predict all the cells without values
        predictions_svd = algo_svd.test(testset)

        # get the top n recommendations for the user of the app. I name it Johnny.
        # a list contains tuples of ('song_id', 'score'), sorted by score
        top_n_svd = self.get_top_n(predictions_svd, targetSongidList, n=10)
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

    def get_top_n(self, predictions, targetSongidList, n=10):
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
            if iid not in targetSongidList:
                top_n[uid].append((iid, est))

        # Then sort the predictions for each user and retrieve the k highest ones.
        for uid, user_ratings in top_n.items():
            user_ratings.sort(key=lambda x: x[1], reverse=True)
            top_n[uid] = user_ratings[:n]

        return top_n

if __name__=='__main__':
    targetSongidList = ['SOAKIMP12A8C130995','SOBBMDR12A8C13253B','SOBXHDL12A81C204C0','SOBYHAJ12A6701BF1D','SODACBL12A8C13C273']

    # create svd object
    svd = mySVD()

    # create testdata and transform into the required format from the recommender package
    newObs = svd.createNewObs(targetSongidList)
    testset = svd.testGenerator(newObs)

    # get training data and transform into the required format from the recommender package
    song_df = svd.readSongData()
    trainset = svd.trainGenerator(song_df, newObs)

    # fit model
    algo_svd = svd.fitModel(trainset)

    # make final recommendation
    user_recommend = svd.predictTopSong(algo_svd, testset, targetSongidList)


    # # data = svd.readSurpriseFormat(newObs)
    # user_recommend = svd.fitModel(data)
    #


