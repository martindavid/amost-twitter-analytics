## TODO
- add provisioning of all 3 machines with the right software for each.
- Change instance flavour from ```m2.tiny``` to ```m2.medium```.
---

Ensure that:
- Private key exists: ```~/.ssh/amost-1.pem```
- It is added to the SSH agent: ```ssh-agent bash; ssh-add ~/.ssh/amost-1.pem```

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
- _ping all hosts_
- _format + mount volume_ [all]
    ```bash
    sudo mkfs.ext4 /dev/vdb
    sudo mkdir /mnt/storage
    sudo mount /dev/vdb /mnt/storage
    ```
- _install CouchDB 1.6_ [harvester + analyser]
    ```bash
    sudo add-apt-repository ppa:couchdb/stable
    sudo apt-get install couchdb

    sudo chown -R couchdb:couchdb /usr/bin/couchdb /etc/couchdb /usr/share/couchdb
    sudo chmod -R 0777 /usr/bin/couchdb /etc/couchdb /usr/share/couchdb
    sudo systemctl restart couchdb
    ```
    - _change WD of CouchDB to volume_
    ```bash
    curl -X PUT http://localhost:5984/_config/couchdb/database_dir -d '"/mnt/storage/couchdb"'
    curl -X PUT http://localhost:5984/_config/couchdb/view_index_dir -d '"/mnt/storage/couchdb"'
    ```
- _install PostgreSQL_  [harvester]
    - DB: ```amost_twitter```
    - UN: ```twitter```
    - PW: ```amost-1```

- download harvester appl from GitHub   [harvester]
    ```bash
    sudo apt-get install python3-pip
    sudo pip install virtualenv
    
    git clone https://github.com/martindavid/amost-twitter-analytics.git
    # This needs a username/pass as repo is private
    # Use SSH key

    cd amost-twitter-analytics/twitter-harvester
    sudo pip install -r requirements.txt
    
    # sudo -u postgres createdb amost_twitter
    # sudo -u postgres createuser -P -s -e twitter
    #This requires a password; maybe not needed if Ansible works

    
    sudo -u postgres psql -f db_structure/create.sql amost_twitter
    sudo -u postgres psql -f db_structure/keyword.sql amost_twitter
    sudo -u postgres psql -f db_structure/twitter_token.sql amost_twitter

- fill up send .env file for twitter-harvester
    
<br><br><br><br><br>

- launch harvester
    ```bash
    nohup <file>.py &
    ```
- setup **replication** between CouchDB on ```harvester``` and ```analyser```

- install ```nginx``` on webserver
    ```bash
    # Install
    sudo apt-get install nginx

    # Set firewall rules
    sudo ufw allow 'Nginx HTTP'
    ```

_Italics_ refer to tasks that have been implemented.