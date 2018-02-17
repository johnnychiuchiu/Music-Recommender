# from sklearn.metrics import mean_squared_error
# from sklearn.cross_validation import train_test_split
import pandas as pd
import numpy as np
import os
import sqlite3

import argparse

class collaborativeFiltering():
    def __init__(self):
        pass



    def readSongData(self, top):
        """
        Read song data from database
        """

        path = os.getcwd() + '/../../data/song.sqlite'
        print(path)
        conn = sqlite3.connect(path)
        song_df = pd.read_sql_query("SELECT * FROM Song;", conn)

        # keep top_n rows of the data
        song_df = song_df.head(top)

        song_df = self.drop_freq_low(song_df)

        return(song_df)

    def drop_freq_low(self, song_df):
        freq_df = song_df.groupby(['user_id']).agg({'song_id': 'count'}).reset_index(level=['user_id'])
        below_userid = freq_df[freq_df.song_id <= 5]['user_id']
        new_song_df = song_df[~song_df.user_id.isin(below_userid)]

        return(new_song_df)

    def utilityMatrix(self, song_df):
        """
        Transform dataframe into utility matrix, return both dataframe and matrix format
        :param song_df: a dataframe that contains user_id, song_id, and listen_count
        :return: dataframe, matrix
        """
        song_reshape = song_df.pivot(index='user_id', columns='song_id', values='listen_count')
        song_reshape = song_reshape.fillna(0)
        ratings = song_reshape.as_matrix()
        return(song_reshape, ratings)

    def fast_similarity(self, ratings, kind='user', epsilon=1e-9):
        """
        Calculate the similarity of the rating matrix
        :param ratings: utility matrix
        :param kind: user-user sim or item-item sim
        :param epsilon: small number for handling dived-by-zero errors
        :return: correlation matrix
        """

        if kind == 'user':
            sim = ratings.dot(ratings.T) + epsilon
        elif kind == 'item':
            sim = ratings.T.dot(ratings) + epsilon
        norms = np.array([np.sqrt(np.diagonal(sim))])
        return (sim / norms / norms.T)

    def predict_fast_simple(self, ratings, kind='user'):
        """
        Calculate the predicted score of every song for every user.
        :param ratings: utility matrix
        :param kind: user-user sim or item-item sim
        :return: matrix contains the predicted scores
        """

        similarity = self.fast_similarity(ratings, kind)

        if kind == 'user':
            return similarity.dot(ratings) / np.array([np.abs(similarity).sum(axis=1)]).T
        elif kind == 'item':
            return ratings.dot(similarity) / np.array([np.abs(similarity).sum(axis=1)])

    def get_overall_recommend(self, ratings, song_reshape, user_prediction, top_n=10):
        """
        get the top_n predicted result of every user. Notice that the recommended item should be the song that the user
         haven't listened before.
        :param ratings: utility matrix
        :param song_reshape: utility matrix in dataframe format
        :param user_prediction: matrix with predicted score
        :param top_n: the number of recommended song
        :return: a dict contains recommended songs for every user_id
        """
        result = dict({})
        for i, row in enumerate(ratings):
            user_id = song_reshape.index[i]
            result[user_id] = {}
            zero_item_list = np.where(row == 0)[0]
            prob_list = user_prediction[i][np.where(row == 0)[0]]
            song_id_list = np.array(song_reshape.columns)[zero_item_list]
            result[user_id]['recommend'] = sorted(zip(song_id_list, prob_list), key=lambda item: item[1], reverse=True)[
                                           0:top_n]

        return (result)

    def get_user_recommend(self, user_id, overall_recommend, song_df):
        """
        Get the recommended songs for a particular user using the song information from the song_df
        :param user_id:
        :param overall_recommend:
        :return:
        """
        user_score = pd.DataFrame(overall_recommend[user_id]['recommend']).rename(columns={0: 'song_id', 1: 'score'})
        user_recommend = pd.merge(user_score,
                                  song_df[['song_id', 'title', 'release', 'artist_name', 'song']].drop_duplicates(),
                                  on='song_id', how='left')
        return (user_recommend)

    def createNewObs(self, artistName, song_reshape, index_name):
        """
        Append a new row with userId 0 that is interested in some specific artists
        :param artistName: a list of artist names
        :return: dataframe, matrix
        """
        interest = []
        for i in song_reshape.columns:
            if i in song_df[song_df.artist_name.isin(artistName)]['song_id'].unique():
                interest.append(10)
            else:
                interest.append(0)

        print(pd.Series(interest).value_counts())

        newobs = pd.DataFrame([interest],
                              columns=song_reshape.columns)
        newobs.index = [index_name]

        new_song_reshape = pd.concat([song_reshape, newobs])
        new_ratings = new_song_reshape.as_matrix()
        return (new_song_reshape, new_ratings)

if __name__=='__main__':

    # # take argument from command line
    # # ['Daft Punk', 'John Mayer', 'Hot Chip', 'Coldplay']
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--inputartist', nargs='+', help='<Required> Set flag', required=True)
    # parser.add_argument(
    #     '--outputfile', type=str, help='output prediction file name')
    # args = parser.parse_args()


    # run model
    cf = collaborativeFiltering()
    song_df = cf.readSongData(1000)
    song_reshape, ratings = cf.utilityMatrix(song_df)
    song_reshape, ratings = cf.createNewObs(args.inputartist,
                                            song_reshape, 'Johnny')
    user_prediction = cf.predict_fast_simple(ratings, kind='user')
    user_overall_recommend = cf.get_overall_recommend(ratings, song_reshape, user_prediction, top_n=10)
    user_recommend_johnny = cf.get_user_recommend('Johnny', user_overall_recommend, song_df)
    user_recommend_johnny.to_csv(args.outputfile, sep=',', index=False)
















