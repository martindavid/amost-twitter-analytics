#!/bin/bash

echo "Starting auto-deployment..."

# Create new group in hosts file
echo "[CCC]" >> ./ansible/hosts

# Launch instance, create volume, attach volume...
# ...extract IP addr from stdout and append to hosts
python3 ./boto/CreateInstance.py | grep -Po '(\d{1,3}\.){3}\d{1,3}' >> ./ansible/hosts

# Ping all hosts in new group, without checking new keys
ANSIBLE_HOST_KEY_CHECKING=False ansible CCC -i ./ansible/hosts -m ping


