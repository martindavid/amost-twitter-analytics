**Ensure** that:
- Private key exists: ```~/.ssh/amost-1.pem```
- It is added to the SSH agent: ```ssh-agent bash; ssh-add ~/.ssh/amost-1.pem```
- Python version [3.6](https://www.python.org/downloads/release/python-361/) is installed (for Ansible to [work](https://github.com/ansible/ansible/issues/23680))
    - ensure [zlib is installed](https://stackoverflow.com/questions/12344970/building-python-from-source-with-zlib-support) before making python
- Ansible version 2.3 (or more) is [installed] from [source](https://github.com/ansible/ansible) and the environment [configured](https://github.com/ahes/ansible-filter-plugins/issues/2)
    - $ ```source hacking/env-setup```

Run ```./deploy.sh```
===

## [INFO]

This file performs the following steps in order:
### **BOTO**
Script: ```CreateInstance.py```
- _launch VM_
- _create volume_
- _attach volume to VM_

### **Bash**
 - _retrieve IP address and add to Ansible hosts file_
    
### **Ansible**
---
#### ALL
- _ping all hosts_
- _format + mount volume_ [all]
    ```bash
    sudo mkfs.ext4 /dev/vdb
    sudo mkdir /mnt/storage
    sudo mount /dev/vdb /mnt/storage
    ```
---
#### harvester
- _install CouchDB 1.6_
    ```bash
    sudo add-apt-repository ppa:couchdb/stable
    sudo apt-get install couchdb

    sudo chown -R couchdb:couchdb /usr/exibin/couchdb /etc/couchdb /usr/share/couchdb
    sudo chmod -R 0777 /usr/bin/couchdb /etc/couchdb /usr/share/couchdb
    sudo systemctl restart couchdb
    ```
    - _change WD of CouchDB to volume and remove localhost binding_
    ```bash
    curl -X PUT http://localhost:5984/_config/couchdb/database_dir -d '"/mnt/storage/couchdb"'
    curl -X PUT http://localhost:5984/_config/couchdb/view_index_dir -d '"/mnt/storage/couchdb"'
    curl -X PUT http://localhost:5984/_config/httpd/bind_address -d '"0.0.0.0"'
    ```
- _install PostgreSQL_  [harvester]
    - DB: ```amost_twitter```
    - UN: ```twitter```
    - PW: ```amost-1```

- _download harvester appl from [GitHub](https://github.com/martindavid/amost-twitter-analytics)   [harvester]_
    ```bash
    sudo apt-get install python-pip
    sudo pip install virtualenv
    
    git clone https://github.com/martindavid/amost-twitter-analytics.git
    # Use SSH key ~/.ssh/git.pem

    cd amost-twitter-analytics/twitter-harvester
    sudo pip install -r requirements.txt
    
    # Create correct DB in PSQL
    # sudo -u postgres createdb amost_twitter
    # sudo -u postgres createuser -P -s -e twitter
    
    # Set up PSQL
    sudo -u postgres psql -f db_structure/create.sql amost_twitter
    sudo -u postgres psql -f db_structure/keyword.sql amost_twitter
    sudo -u postgres psql -f db_structure/twitter_token.sql amost_twitter
    sudo -u postgres psql -d amost_twitter -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO twitter;"
- _send .env file for database variables needed by twitter-harvester'_

- _launch harvester_
    ```bash
    nohup python cli.py stream GROUP1 &
    ```
---
#### replica server
- _setup **replication** between CouchDB on ```harvester``` and ```replica```_
    ```bash
    # Insert correct IP of replica VM
    curl -X POST localhost:5984/_replicate -d '{"source":"tweets", "target":"http://<replica_server>:5984/tweets", "continuous":true}' -H "Content-Type:application/json"
    ```
---

#### analyser + webserver

- install ```nginx``` on webserver
    ```bash
    # Install
    sudo apt-get install nginx

    # Set firewall rules
    sudo ufw allow 'Nginx HTTP'
    ```
- install ```nodejs```
    
    ```bash
    # Add correct repo to apt
    curl -sL https://deb.nodesource.com/setup_6.x -o nodesource_setup.sh
    sudo bash nodesource_setup.sh
    
    # install node.js
    sudo apt-get install nodejs

    # install npm
    sudo npm install -g express
    ```

- copy [web app](https://github.com/martindavid/amost-twitter-web)

- install dependencies for app
    ```bash
    # Export env variables
    export COUCHDB_TWEETS='http://127.0.0.1:15984/tweets/'
    export COUCHDB_TWEET_WORDS='http://127.0.0.1:15984/twitter-words/'
    export COUCHDB_TWEET_HASHTAGS='http://127.0.0.1:15984/twitter-hashtags/'
    export COUCHDB_TWEET_USERS='http://127.0.0.1:15984/twitter-users/'

    # Start webserver
    export NODE_ENV='development'
    npm install
    cd client && npm install
    npm run build
    cd ..
    export NODE_ENV='production'
    
    npm install pm2 -g
    pm2 start server.js
    #npm run server
    ```
- copy analyser scripts
---
