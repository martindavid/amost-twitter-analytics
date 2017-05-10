#!/bin/bash

echo "Starting auto-deployment..."

## Spin up DB server
# Create new group in hosts file
echo "[analyser]" >> ./ansible/hosts
# Launch instance, create volume, attach volume...
# ...extract IP addr from stdout and append to hosts
python3 ./boto/CreateInstance.py | grep -Po '(\d{1,3}\.){3}\d{1,3}' >> ./ansible/hosts
echo "Analyser server created."

## Spin up harvester server
# Create new group in hosts file
echo "[harvester]" >> ./ansible/hosts
# Launch instance, create volume, attach volume...
# ...extract IP addr from stdout and append to hosts
python3 ./boto/CreateInstance.py | grep -Po '(\d{1,3}\.){3}\d{1,3}' >> ./ansible/hosts
echo "Harvester server created."

# Pause to allow last VM to become available via SSH
echo "Waiting for 1 minute for the provisioning dust to settle..."
sleep 60

# Ping all hosts in new group, without checking new keys
sudo ANSIBLE_HOST_KEY_CHECKING=False ansible all -i ./ansible/hosts -m ping

# Mount volume storage
sudo ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i ./ansible/hosts ./ansible/playbooks/volume.yml

# Install CouchDB
sudo ansible-playbook -i ./ansible/hosts ./ansible/playbooks/couchdb.yml

# Install PostgreSQL
sudo ansible-playbook -i ./ansible/hosts ./ansible/playbooks/postgre.yml

# Set up and launch harvester from GitHub repo
sudo ansible-playbook -i ./ansible/hosts ./ansible/playbooks/harvester.yml

# Set up Webserver

