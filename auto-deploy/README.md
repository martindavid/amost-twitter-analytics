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
    - DB: ```public```
    - UN: ```amost```
    - PW: ```amostsecretpassword```

- download harvester appl from GitHub   [harvester]
    ```bash
    git clone <repo>
    ```

    - launch harvester
    ```bash
    nohup <file>.py &
    ```
- setup **replication** between CouchDB on ```harvester``` and ```analyser```
- install ```htttpd``` on webserver

_Italics_ refer to tasks that have been implemented.