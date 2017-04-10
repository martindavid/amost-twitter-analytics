# Twitter Harvester

A harvester for twitter data

# Prerequisites Stack
Make sure you have this stack installed on your machine first
- [Postgresql](https://www.postgresql.org/)
- [CouchDB](http://couchdb.apache.org/)
- Python 3.5

# Installation
### Setup Python and VirtualEnv
VirtualEnv is a way to create isolated Python environments for every project and VirtualEnvWrapper "wraps" the virtualenv API to make it more user friendly.

```bash
$ pip install pip --upgrade
$ pip install virtualenv
$ pip install virtualenvwrapper
```

To complete the virtualenv setup process, put the following in you ~/.bash_profile
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

# Usage
Create new file `.env` in the twitter-harvester root folder and put this information:

```
PG_DB_USER='<your postgresql database username>'
PG_DB_PASSWORD='<your postgresql database password>'
PG_DB_NAME='<your postgresql database name>'
COUCHDB_SERVER='<couchdb connection url>' #default 'http://127.0.0.1:5984/'
```

Run the sql script in the `db_structure` folder and fill in the data you need for test.
(TODO: find a better way to distribute the db structure)

To run the app:

    $ python cli.py <type> <group_name>

Example:

    $ python cli.py search GROUP1

