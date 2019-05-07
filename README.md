
# hotels-page-analyser

## About Project

### Directory Tree

├── app.py
├── dataset
│   └── sites.csv
├── models
│   ├── about_pages_model.pkl
│   └── privacy_pages_model.pkl
├── page_analyser.py
├── page_classifier.py
├── README.md
└── requirements.txt

## Getting Started

### Clone
Download the repository on your machine using the `git clone` command as seen below:  

```git clone git@github.com:HAKSOAT/hotels-page-analyser.git```

Change into the cloned directory to proceed:  

`cd hotels-page-analyser`

### Install Dependencies
Install the dependencies using `pip` and the `requirements.txt` file with the command below:  

`pip install -r requirements.txt`

**NB**: The software is written to be Python3 compatible, using with Python2 may give undesirable results.

## Running the Script

### Predicting Pages

To predict the classes of pages, simply pass in the base url of the site you want to classify:  

```
python app.py --predict "http://example.com/"
```

It'll take a while, but you'll get similar results this:  

```
Getting metadata, this may take a while.
http://company.trivago.com/our-story ===>>> About Page
http://company.trivago.com/privacy-policy ===>>> Privacy Page
```

The above results were gotten after running on the url `http://company.trivago.com`

Models are available to be used, hence you do not need to train a model before running code.

### Training Models

If you intend training your own models, you can either retrain using `sites.csv` file, and also choose how many links you intend training the model on.  
  
**Fetching links and training models takes time; so do this only if you understand what you are doing.**

To train the models based on the `sites.csv` file, run the following:

```
python app.py --train sites.csv --number 20
```

The command above will train the models using the first 20 links from the dataset.

**Every train attempt overwrites the models previously trained**

## Credits

Credits go to [HotelsNG](https://hotels.ng) for giving the interns a platform to work on this project, and every intern that contributed to it.

Credits also go to the authors of the paper [Automatic Web Page Categorization UsingMachine Learning and Educational-Based Corpus](http://www.ijcte.org/vol9/1180-IT026.pdf); it was key in helping the interns understand the kind of problems that need a web page classifier and how to go about implementing the solution.
