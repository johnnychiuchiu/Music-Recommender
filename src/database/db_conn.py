import sqlite3

def dbConn(path):
    """
    conn to sqlite database


    Parameters
    ----------
    path : chr
        path to the sqlite database

    Returns
    -------
    sqlite object
        sqlite database connection object
    """
    song_db = '../../data/song.sqlite'
    conn = sqlite3.connect(path)
    return conn