## TODO
- Add arguments to script to run ```CreateInstance.py``` **N** times for each machine.
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
- _format + mount volume_ 
    ```bash
    sudo mkfs.ext4 /dev/vdb
    sudo mkdir /mnt/storage
    sudo mount /dev/vdb /mnt/storage
    ```
- _install CouchDB 1.6_
- install PostgreSQL
- change WD of both onto volume

- download harvester appl from GitHub
- launch harvester

_Italics_ refer to tasks that have been implemented.