import os
import sqlite3

from flask import request, render_template
from form.multiselect import ArtistForm
from web import app

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
    path = os.getcwd() + '/data/song.sqlite'
    conn = sqlite3.connect(path)
    cursor = conn.execute('SELECT distinct(title) FROM Song limit 100;')
    return render_template('index.html', songs=cursor.fetchall())


@app.route('/current', methods=['GET', 'POST'])
def current():
    form = ArtistForm(request.form)

    if request.method == 'POST' and form.validate():
        print("POST request and form is valid")
        artist = form.artist.data
        print("languages in wsgi.py: %s" % request.form['artist'])
        return render_template('playlist.html', artist=artist)
    else:
        return render_template('select_form.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)


# from flask import render_template, redirect, request, url_for, session, jsonify
# # a page shows all the
# @app.route('/select', methods=['GET', 'POST'])
# def select():
#     """
#     Returns
#     -------
#     A page shows all the song/artist pairs for user to select.
#     """
#
#     form = ExampleForm()
#     if request.method == 'POST' and form.validate():
#         messages = ['john mayer', 'Coldplay']
#         # messages = form.example.data
#         print(messages)
#         # print(form.example.choices.data)
#         # messages = dict(form.example.choices).get(form.example.choices.data)
#         # print(messages)
#         #session['messages'] = messages
#         return redirect(url_for('.playlist', artists=messages))
#     return render_template('select_form.html', title='Music Recommender', form=form)
#
# @app.route('/playlist', methods=['GET', 'POST'])
# def playlist():
#     """
#     Returns
#     -------
#     A page shows the recommended playlist according to user input.
#     """
#     messages = request.args.get('artists')
#     # messages = request.args['messages']  # counterpart for url_for()
#     # messages = session['messages']
#     print(messages)
#
#     # back = backForm()
#     # form = ExampleForm()
#     # if request.method == 'POST':
#     #     return redirect('/select')
#     return render_template('playlist.html', title='Music Recommender', artists=messages) #,form=back,







