from flask import request, render_template
from form.multiselect import ArtistForm
from web import application
from src.models.svd import mySVD
import logging



@application.route('/', methods=['GET', 'POST'])
def index():
    # set up logging parameters
    logging.basicConfig(filename='./log/app.log',
                        format='%(asctime)s %(levelname)s:%(message)s',
                        level=logging.DEBUG)

    form = ArtistForm(request.form)

    if request.method == 'POST' and form.validate():
        logging.debug('POST request and form is valid')
        artist = form.artist.data
        logging.debug('Song ID:'+', '.join(map(str, artist)))

        # run SVD model
        # create svd object
        logging.debug("Create svd object")
        svd = mySVD()

        # create test data and transform into the required format from the recommender package
        logging.debug("Create test data")
        newObs = svd.createNewObs(artist)
        testset = svd.testGenerator(newObs)

        # get training data and transform into the required format from the recommender package
        logging.debug("Get training data")
        trainset = svd.trainGenerator(svd.song_df, newObs)

        # fit model
        logging.debug("Fit recommender model")
        algo_svd = svd.fitModel(trainset)

        # make final recommendation
        logging.debug("Generate top 10 recommendation")
        user_recommend = svd.predictTopSong(algo_svd, testset, artist)

        return render_template('playlist.html', artists=user_recommend.to_html(), artist=artist)
    else:
        return render_template('select_form.html', form=form)


if __name__ == '__main__':
    application.run(host='0.0.0.0')
