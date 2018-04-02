import pandas as pd
from surprise import Dataset
from surprise import Reader
from surprise import SVD
from collections import defaultdict
import pymysql
import yaml
import os

class mySVD():
    """
    Build a recommender system using Singular Value Decomposition Method
    Implemented using Surprise Package
    """
    def __init__(self):
        model_meta = self.getParams()

        self.DEFAULT_COUNT = model_meta['data_manipulate']['default_count']
        self.song_df = self.readSongData()
        self.songidList = list(self.song_df['song_id'].unique())

        self.N_FACTORS = model_meta['svd']['n_factors']
        self.LR_ALL = model_meta['svd']['lr_all']
        self.REG_ALL = model_meta['svd']['reg_all']
        self.SEED = model_meta['svd']['seed']


    def getParams(self):
        """Get params for model building"""
        print(os.getcwd())
        with open('params.yaml', 'r') as f:
            model_meta = yaml.load(f)

        return model_meta


    def readSongData(self):
        """
        Read song data from database

        Args:
            top (int): random sample n users from song_df

        Returns:
            pd.DataFrame: a pandas dataframe with columns 'user_id', 'song_id', 'listen_count', 'title', 'release',
                        'artist_name', 'year', 'song'

        """

        # try just using real host and everything
        conn = pymysql.connect("dbmarch9.c7rrmd1b0hyo.us-west-2.rds.amazonaws.com",
                               user="usermarch9",
                               port=3306,
                               passwd="12345678",
                               db="dbmarch9")

        song_df = pd.read_sql('SELECT * FROM Song;', con=conn)

        return song_df

    def trainGenerator(self, song_df, newObs):
        """
        transform the song dataframe into the required format for the Surprise package

        Args:
            song_df (pd.DataFrame): dataframe obtained from readSongData method
            newObs (pd.DataFrame):

        Returns:
            surprise.trainset.Trainset: training data in the Surprise package format
        """
        train = song_df[['user_id', 'song_id', 'listen_count']]

        # A reader is still needed but only the rating_scale param is requiered.
        reader = Reader(line_format='user item rating', rating_scale=(1, 100))
        trainset_load = Dataset.load_from_df(pd.concat([train,newObs]), reader)
        trainset = trainset_load.build_full_trainset()
        return trainset

    def testGenerator(self, df):
        """
        transform testing dataframe into the required format for the Surprise package

        Args:
            df (pd.DataFrame): testing data in the dataframe format

        Returns:
            list:
                testing data in the required format for the Surprise package
                the required format is list of tuples with user, song, and count
        """

        return [(uid, iid, r) for (uid, iid, r) in zip(df['user_id'], df['song_id'], df['listen_count'])]

    def createNewObs(self, targetSongidList):
        """
        Append a new row with userId Johnny that is interested in a selected list of songs

        Args:
            targetSongidList (list): the user selected song_ids with format like `SOAKIMP12A8C130995`

        Returns:
        pd.DataFrame: a pandas dataframe with columns 'user_id', 'song_id', 'listen_count'

        """

        newObs = pd.DataFrame({'user_id': ['johnny'] * len(self.songidList),
                                'song_id': self.songidList,
                                'listen_count': 0})[['user_id', 'song_id', 'listen_count']]

        mask = newObs['song_id'].isin(targetSongidList)
        column_name = 'listen_count'
        newObs.loc[mask, column_name] = self.DEFAULT_COUNT

        return newObs

    def fitModel(self, trainset):
        """
        train a recommender system using SVD with pre-defined parameters

        Args:
            data (surprise.trainset.Trainset):
                a surprise.trainset object obtained from the method trainGenerator

        Returns
        -------
        surprise.prediction_algorithms.matrix_factorization.SVD: an SVD object from the Surprise package

        """

        # fit model using parameters tuned using 2000 user_id
        algo_svd = SVD(n_factors=self.N_FACTORS, lr_all=self.LR_ALL, reg_all=self.REG_ALL, random_state=self.SEED)
        algo_svd.fit(trainset)

        return algo_svd

    def predictTopSong(self, algo_svd, testset, targetSongidList):
        """
        get the top 10 song prediction using the input recommender system object for the user in the testset and
        the song in the targetSongidList

        Args:
            algo_svd (surprise.prediction_algorithms.matrix_factorization.SVD):
                an SVD object from the Surprise package
                this can be obtained from the method fitModel
            testset (list):
                testing data in the required format for the Surprise package
                this can be obtained from the method testGenerator
            targetSongidList (list): the user selected song_ids with format like `SOAKIMP12A8C130995`

        Returns:

        """

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

        Args:
            top_list (list): a list contains tuples of ('song_id', 'score'), sorted by score

        Returns:
        pd.DataFrame: A dataframe containing the songs in the top_list, sorted by score.
        """

        user_score = pd.DataFrame(top_list).rename(columns={0: 'song_id', 1: 'score'})
        user_recommend = pd.merge(user_score,
                                  self.song_df[['song_id', 'title', 'release', 'artist_name', 'song']].drop_duplicates(),
                                  on='song_id', how='left')
        return user_recommend

    def get_top_n(self, predictions, targetSongidList, n=10):
        """
        Return the top-N recommendation for each user from a set of predictions.

        Args:
            predictions (list):
                The list of predictions, as returned by the test method of an recommender system object from Surprise.
            n (int): the number of recommendation to output for each user. Default is 10.

        Returns:
        dict:
            A dict where keys are user (raw) ids and values are lists of tuples: [(raw item id, rating estimation), ...]
            of size n.
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
    trainset = svd.trainGenerator(svd.song_df, newObs)

    # fit model
    algo_svd = svd.fitModel(trainset)

    # make final recommendation
    user_recommend = svd.predictTopSong(algo_svd, testset, targetSongidList)
    print(user_recommend)
