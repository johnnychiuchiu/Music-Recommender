from flask import render_template
import sqlite3
from database.schema import Song
from web import app
from database.db_conn import dbConn


# Create view into index page that uses data queried from Track database
# and inserts it into the msiapp/templates/index.html template
@app.route('/')
def index():
    # return render_template('index.html', songs=Song.query.first())
    conn = dbConn('../develop/data/song.sqlite')
    cursor = conn.execute('SELECT * FROM Song limit 100;')
    return render_template('index.html', songs=cursor.fetchall())




if __name__ == "__main__":
    app.run(debug=True)
