Ensure that:
- Private key exists: ```~/.ssh/amost-1.pem```
- It is added to the SSH agent: ```ssh-agent bash; ssh-add ~/.ssh/amost-1.pem```

Run ```./deploy.sh```
===

This file performs the following steps in order:
## BOTO
Script: ```CreateInstance.py```
- _launch VM_
- _create volume_
- _attach volume to VM_

## Bash
 - _retrieve IP address and add to Ansible hosts file_
    
## Ansible
- _ping all hosts_
- format volume
- mount volume
- install CouchDB
- install PostgreSQL
- change WD of both onto volume

- download harvester appl from GitHub
- launch harvester
