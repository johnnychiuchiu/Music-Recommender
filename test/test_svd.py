import pandas as pd
import sys
sys.path.append('../')
from src.models.svd import mySVD
import surprise

# set testing cases
targetSongidList = ['SOAKIMP12A8C130995','SOBBMDR12A8C13253B','SOBXHDL12A81C204C0','SOBYHAJ12A6701BF1D','SODACBL12A8C13C273']

# create svd object
svd = mySVD()

# create testdata and transform into the required format from the recommender package
newObs = svd.createNewObs(targetSongidList)
testset = svd.testGenerator(newObs)

# transform into the required format from the recommender package
trainset = svd.trainGenerator(svd.song_df, newObs)

# fit model
algo_svd = svd.fitModel(trainset)

# make final recommendation
user_recommend = svd.predictTopSong(algo_svd, testset, targetSongidList)



def test_readSongData():
    """Test method readSongData from class mySVD"""

    # make sure the number of columns pull out from the database is correct
    assert svd.song_df.shape[1] == 8


def test_createNewObs():
    """Test method createNewObs from class mySVD"""

    # check type
    assert isinstance(newObs, pd.DataFrame)

    # check if there are exactly 5 songs has listen count and 3 columns in the generated df
    assert newObs.query("listen_count!=0").shape == (5,3)

    # check if the number of songs in the song_df is the same as the generated new df
    assert len(svd.song_df.song_id.unique()) == len(newObs.song_id.unique())

def test_testGenerator():
    """Test method testGenerator from class mySVD"""

    # check type
    assert isinstance(testset, list)

    # check the shape
    assert len(testset)==newObs.shape[0]


def test_trainGenerator():
    """Test method trainGenerator from class mySVD"""

    # check type
    assert isinstance(trainset, surprise.trainset.Trainset)

    # the number of users in trainset should be equal to the user from database plus 1
    assert len(trainset.all_users()) == len(svd.song_df.user_id.unique())+1


def test_fitModel():
    """Test method fitModel from class mySVD"""

    # check type
    assert isinstance(algo_svd, surprise.prediction_algorithms.matrix_factorization.SVD)


def test_predictTopSong():
    """Test method predictTopSong from class mySVD"""

    user_recommend = svd.predictTopSong(algo_svd, testset, targetSongidList)

    # check type
    assert isinstance(user_recommend, pd.DataFrame)

    # check shape
    assert user_recommend.shape == (10, 6)

    # check sorted
    assert user_recommend.loc[0]['score'] == max(user_recommend.score)


