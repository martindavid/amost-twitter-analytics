# Analytics Part

A collection of manual and automatic analytics script that we use for twitter analysis.

# Prerequisites Stack
- Make sure you have an access to CouchDB
- Python 2.7+

# Getting started
### Setup Python and VirtualEnv
VirtualEnv is a way to create isolated Python environments for every project and VirtualEnvWrapper "wraps" the virtualenv API to make it more user friendly.

```bash
$ pip install pip --upgrade
$ pip install virtualenv
$ pip install virtualenvwrapper
```

To complete the virtualenv setup process, put the following in your ~/.bash_profile
```bash
export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh
```

Create your virtual environment to run this analysis code and install all of the packages needed

    $ mkvirtualenv amost-analysis
    $ pip install -r requirements.txt

# Code Structure

General Twitter Analysis
------------------------

- TweetAnalytics.ipynb

This section is for pre-eliminary analysis for general twitter analysis. The analysis is in Python Jupyter Notebook that contains analysis for:

#### User analysis (gender prediction)
For this analysis we use [genderComputer](https://github.com/tue-mdse/genderComputer) library to predict the gender based on user provided name

#### Twitter Text Analysis
- Terms frequency
- Hashtags frequency




Regression Analysis
-------------------

- regressionAnalysis.ipynb

This section contains Python Jupyter Notebook for the analysis of the tweets harvested, focusing only on Victoria.

The topic of analysis concerns correlation between the positive, negative, and food-related tweets count and premature mortality (total) and premature mortality from heart disease

tunnelling (L5984) between the VM with CouchDB is required if you want to run the script again, otherwise, the output is recorded in the script.
