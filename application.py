from flask import request, render_template
from form.multiselect import ArtistForm
from web import application
from src.models.svd import mySVD


@application.route('/', methods=['GET', 'POST'])
def index():
    form = ArtistForm(request.form)

    if request.method == 'POST' and form.validate():
        print("POST request and form is valid")
        artist = form.artist.data
        print(artist)
        print("languages in wsgi.py: %s" % request.form['artist'])

        # run SVD model
        # create svd object
        svd = mySVD()

        # create test data and transform into the required format from the recommender package
        newObs = svd.createNewObs(artist)
        testset = svd.testGenerator(newObs)

        # get training data and transform into the required format from the recommender package
        song_df = svd.readSongData()
        trainset = svd.trainGenerator(song_df, newObs)

        # fit model
        algo_svd = svd.fitModel(trainset)

        # make final recommendation
        user_recommend = svd.predictTopSong(algo_svd, testset, artist)

        return render_template('playlist.html', artists=user_recommend.to_html(), artist=artist)
    else:
        return render_template('select_form.html', form=form)


if __name__ == '__main__':
    application.run(host='0.0.0.0')
