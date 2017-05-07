#!/bin/bash

echo "Starting auto-deployment..."

## Spin up DB server
# Create new group in hosts file
echo "[DB]" >> ./ansible/hosts
# Launch instance, create volume, attach volume...
# ...extract IP addr from stdout and append to hosts
python3 ./boto/CreateInstance.py | grep -Po '(\d{1,3}\.){3}\d{1,3}' >> ./ansible/hosts
echo "\n" >> ./ansible/hosts

## Spin up harvester server
# # Create new group in hosts file
# echo "[HARVEST]" >> ./ansible/hosts
# # Launch instance, create volume, attach volume...
# # ...extract IP addr from stdout and append to hosts
# python3 ./boto/CreateInstance.py | grep -Po '(\d{1,3}\.){3}\d{1,3}' >> ./ansible/hosts
# echo "\n" >> ./ansible/hosts

# Ping all hosts in new group, without checking new keys
ANSIBLE_HOST_KEY_CHECKING=False ansible all -i ./ansible/hosts -m ping

# Mount volume storage
ansible-playbook -i ./ansible/hosts ./ansible/playbooks/volume.yaml

