# Music-Recommender
[![license](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/johnnychiuchiu/Machine-Learning/blob/master/LICENSE)

* **Vision**: Engage music fans by recommending select number of songs based on user’s song and genre preference.
* **Mission**: The goal of the project is to help people discover the music they may enjoy by providing them a list of recommended songs according to their favorite musicians and songs. This will be done using a collaborative filtering or a latent factor recommender model that is trained with the [Million Song Dataset](https://www.google.com/search?q=million+song+dataset&oq=million+so&aqs=chrome.0.69i59j69i60l2j69i61j69i57j0.5455j0j7&sourceid=chrome&ie=UTF-8).
* **SuccessCriteria**: Successfully deployed a web application that dynamically shows a recommended list of songs according to users’ input.


Steps
------------

**Environment**
* Go to `Music-Recommender/` folder, run
```
> source ./py/bin/activate
> pip install -r requirement.txt
```

**Get Data**

* Go to `src/database` folder, run the following command. The data will be populated under `Music-Recommender/data` folder 
```
> python create_db.py
> python insert_data.py
```

**Run App**
* Go to `Music-Recommender/` folder, run
```
> python app.py
```


Documentation
------------
* `latentFactorModel.ipynb`: Jupyter Notebook that contains a walkthrough of the overall process. [[jupyter notebook](https://github.com/johnnychiuchiu/Music-Recommender/blob/sprint_1/develop/notebooks/latentFactorModel.ipynb)]


Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data               <- Data files
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py





