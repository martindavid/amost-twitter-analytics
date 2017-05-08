# Twitter Harvester

A harvester for twitter data

# Prerequisites Stack
Make sure you have this stack installed on your machine first
- [Postgresql](https://www.postgresql.org/)
- [CouchDB](http://couchdb.apache.org/)
- [PSequel](http://www.psequel.com/) => If you don't want to manage your postgresql from command line
- Python 3.5

# Installation
### Install PostgreSQL using brew
Thanks God if you're on osx machine, just run this command to install it:
```bash
$ brew install postgresql
```

After it succesfully installed, start the service by:
```bash
$ brew services start postgresql
```

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

### Create VirtualEnv and Install Dependencies
The following commands will ensure you have the Python dependencies installed inside your `virtualenv`.

```bash
mkvirtualenv amost-project --python=python3
pip install -r requirements.txt
```

### Run Database Structure Creation
Run `create.sql` file under db_structure folder to initiate the postgresql structure for the first time (make sure your postgresql database is running)

### Initial data setup
* Use psequel to easily insert/update postgresql data
* Get twitter API token from [twitter developer](https://dev.twitter.com/)
* Put twitter api token information inside `twitter_token` table


#### Run it from command line

```bash
# create new database name amost_twitter
$ createdb amost_twitter

# run create.sql file
$ psql -f db_structure/create.sql amost_twitter
```

# Usage
Create new file `.env` in the twitter-harvester root folder and put this information:

```
PG_DB_USER='<your postgresql database username>'
PG_DB_PASSWORD='<your postgresql database password>'
PG_DB_NAME='<your postgresql database name>'
COUCHDB_DB='tweets'
COUCHDB_SERVER='<couchdb connection url>' #default 'http://127.0.0.1:5984/'
GEO_CODE='-26.288798,134.494629,1500km' # our search area 
```

Run the sql script in the `db_structure` folder and fill in the data you need for test.

To run the app:

    $ python cli.py <type> <group_name>

Example:

### Search API

    $ python cli.py search GROUP1

### Stream API

    $ python cli.py stream GROUP1