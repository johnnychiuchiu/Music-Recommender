from schema import db
# from schema.db_models import *

if __name__=='__main__':
    # create a new table scheme as defined in the schema script
    db.create_all()

