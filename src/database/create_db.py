from schema import db
# from schema.db_models import *

if __name__=='__main__':
    # create song.sqlite under data folder
    db.create_all()

