# Music-Recommender
[![license](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/johnnychiuchiu/Machine-Learning/blob/master/LICENSE)

* **Vision**: Engage music fans by recommending select number of songs based on user’s song and genre preference.
* **Mission**: The goal of the project is to help people discover the music they may enjoy by providing them a list of recommended songs according to their favorite musicians and songs. This will be done using a collaborative filtering or a latent factor recommender model that is trained with the [Million Song Dataset](https://www.google.com/search?q=million+song+dataset&oq=million+so&aqs=chrome.0.69i59j69i60l2j69i61j69i57j0.5455j0j7&sourceid=chrome&ie=UTF-8).
* **SuccessCriteria**: Successfully deployed a web application that dynamically shows a recommended list of songs according to users’ input.


Steps
------------

# Set up Environment
# Go to `Music-Recommender/` folder, run
> source ./py/bin/activate
> pip install -r requirement.txt

# Get Data. After the following command, the data will be populated under `Music-Recommender/data` folder 
> cd ./src/database
> python create_db.py
> python insert_data.py

# Run App
> cd ../..
> python app.py
```


Application Screenshot
------------

![](https://github.com/johnnychiuchiu/Music-Recommender/blob/refactor/directory/pic/page1.png)


![](https://github.com/johnnychiuchiu/Music-Recommender/blob/refactor/directory/pic/page2.png)


Documentation
------------
* `modelSelectionAndTuning.ipynb`: Jupyter Notebook that contains a walkthrough of the overall model building, model selection and parameter tuning. [[jupyter notebook](https://github.com/johnnychiuchiu/Music-Recommender/blob/refactor/directory/src/notebooks/modelSelectionAndTuning.ipynb)]

* `latentFactorModel.ipynb`: An old version of the overall model building process [[jupyter notebook](https://github.com/johnnychiuchiu/Music-Recommender/blob/sprint_1/develop/notebooks/latentFactorModel.ipynb)]


Project Organization
------------

    ├── LICENSE
    │
    ├── README.md          <- The top-level README for developers using this project.
    │    
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g. generated with `pip freeze > requirements.txt`               
    │
    ├── py                 <- virtualenv files
    │
    ├── pic                <- some picture for demo purpose
    │
    ├── web                <- HTML and CSS files
    │    
    ├── form               <- user form selection files
    │   
    ├── data               <- Data files
    │
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── database       <- Scripts to download and generate data
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make predictions
    │   │   │                 
    │   │   ├── svd.py
    │   │   └── ubcf.py
    │   │
    │   └── notebooks      <- Jupyter notebooks. Used to reate exploratory, results oriented visualizations,  and parameter tuning                     
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details




