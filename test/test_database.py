import pandas as pd
import sys
sys.path.append('../')
from src.database.insert_data import ReadData


# Set testing objects
# read song data as dataframe
song_df = ReadData().readSongData()

# random sample n users
random_song_df = ReadData().random_select_user(song_df, 10)


def test_readSongData():
    """Test method readSongData from class ReadData"""

    # check type
    assert isinstance(song_df, pd.DataFrame)

    # check shape
    assert song_df.shape == (1972060, 8)


def test_random_select_user():
    """Test method random_select_user from class ReadData"""

    # check type
    assert isinstance(random_song_df, pd.DataFrame)

    # check shape
    assert random_song_df.shape == (739, 8)

    # check number of random users
    assert len(random_song_df.user_id.unique()) == 10

