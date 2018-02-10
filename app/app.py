from flask import render_template, redirect, request
# from flask import flash, render_template, request, redirect
import sqlite3
from database.schema import Song
from web import app
from database.db_conn import dbConn
from multiselect import ExampleForm, backForm

# Create view into index page that uses data queried from Track database
# and inserts it into the msiapp/templates/index.html template
@app.route('/')
def index():
    """
    Returns
    -------
    A page shows all the data as output
    """
    # return render_template('index.html', songs=Song.query.first())
    conn = dbConn('../develop/data/song.sqlite')
    cursor = conn.execute('SELECT distinct(title) FROM Song limit 100;')
    return render_template('index.html', songs=cursor.fetchall())


# a page shows all the
@app.route('/select', methods=['GET', 'POST'])
def select():
    """
    Returns
    -------
    A page shows all the song/artist pairs for user to select.
    """
    form = ExampleForm()
    if request.method == 'POST':
        return redirect('/playlist')
    return render_template('select_form.html', title='Music Recommender', form=form)

@app.route('/playlist', methods=['GET', 'POST'])
def playlist():
    """
    Returns
    -------
    A page shows the recommended playlist according to user input.
    """
    back = backForm()
    # form = ExampleForm()
    if request.method == 'POST':
        return redirect('/select')
    return render_template('playlist.html', title='Music Recommender', form=back)


if __name__ == "__main__":
    app.run(debug=True)
