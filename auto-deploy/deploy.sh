#!/bin/bash

source ~/ansible/hacking/env-setup
ansible --version
echo "Ansible is installed and working."

echo "Starting auto-deployment..."

# # Spin up DB server
# # Create new group in hosts file
# echo -e "\n[analyser_web]" >> ./ansible/hosts
# # Launch instance, create volume, attach volume...
# # ...extract IP addr from stdout and append to hosts
# python3 ./boto/CreateInstance.py | grep -Po '(\d{1,3}\.){3}\d{1,3}' >> ./ansible/hosts
# echo "Analyser/Web server created."

## Spin up harvester server
# Create new group in hosts file
echo -e "\n[harvester]" >> ./ansible/hosts
# Launch instance, create volume, attach volume...
# ...extract IP addr from stdout and append to hosts
python3 ./boto/CreateInstance.py | grep -Po '(\d{1,3}\.){3}\d{1,3}' >> ./ansible/hosts
echo "Harvester server created."

## Spin up DB Replica server
# Create new group in hosts file
echo -e "\n[db_replica]" >> ./ansible/hosts
# Launch instance, create volume, attach volume...
# ...extract IP addr from stdout and store for later
python3 ./boto/CreateInstance.py | grep -Po '(\d{1,3}\.){3}\d{1,3}' > replica_ip

# keep track of replica server's IP for later use
IP=$(cat replica_ip)
echo $IP >> ./ansible/hosts
echo "DB Replica created."

# Pause to allow last VM to become available via SSH
echo "Waiting for 1 minute for the provisioning dust to settle..."
sleep 60

# Ping all hosts in new group, without checking new keys
ANSIBLE_HOST_KEY_CHECKING=False ansible all -i ./ansible/hosts -m ping

# Mount volume storage; all
ansible-playbook -i ./ansible/hosts ./ansible/playbooks/volume.yml

# Install CouchDB; harvester and analyser
ansible-playbook -i ./ansible/hosts ./ansible/playbooks/couchdb.yml

# Install PostgreSQL; harvester only
ansible-playbook -i ./ansible/hosts ./ansible/playbooks/postgre.yml

# Set up/launch harvester from GitHub repo + add replication; harvester only
ansible-playbook -i ./ansible/hosts ./ansible/playbooks/harvester.yml --extra-vars "replica_server=$IP"

# Set up Webserver
# ansible-playbook -i ./ansible/hosts ./ansible/playbooks/webserver.yml
