#!/bin/bash

echo "115.146.86.215" >> ip.file
IP=$(cat ip.file)



ansible-playbook -i ./ansible/hosts ./ansible/playbooks/harvester.yml --extra-vars "replica_server=$IP"
