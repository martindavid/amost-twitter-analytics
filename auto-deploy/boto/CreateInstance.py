#!/usr/bin/env python3

"""
Boto script to provision an instance on NeCTAR Research Cloud
@author: abhi
S1, 2017
"""

import boto
from boto.ec2.regioninfo import RegionInfo

#----Customizable Info-----
#Instance region and NeCTAR API address
API_ENDPOINT = 'nova.rc.nectar.org.au'
API_REGION = 'melbourne-np'
API_PORT = 8773

#NeCTAR account details
ACCESS_KEY_ID = '7abc3190c5174cbaaff56f5d0dc8495a'
SECRET_ACCESS_KEY = '1ffe7072e5c449caba861460179435ea'

#Instance details
KEY = 'abhi-1'
I_TYPE = 'm2.tiny'
SEC_GROUP = ['ssh']
IMAGE = 'ami-c163b887'
    #NeCTAR Ubuntu 16.04 LTS (Xenial) amd64 (pre-installed murano-agent)
#--------------------------

def connect_to_api():
    """
    Connecting to cloud API
    """
    conn = boto.connect_ec2(
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=SECRET_ACCESS_KEY,
        is_secure=True,
        region=RegionInfo(name=API_REGION, endpoint=API_ENDPOINT),
        port=API_PORT,
        path='/services/Cloud',
        validate_certs=False)
    return conn

def print_premade_images(api_conn):
    '''
    Check which pre-made images are possible
    '''
    images = api_conn.get_all_images()
    for img in images:
        print('id: ', img.id, 'name: ', img.name)

def create_instance(api_connection):
    """
    Creates an instance on the cloud
    """
    api_connection.run_instances(
        IMAGE,
        key_name=KEY,
        instance_type=I_TYPE,
        security_groups=SEC_GROUP)

def main():
    """
    Main func
    """
    api_conn = connect_to_api()
    create_instance(api_conn)
    print("Instance spun up.")

    #Get all instances details
    reservations = api_conn.get_all_reservations()


if __name__ == '__main__':
    main()

#======================


#Show reservation details
print ("The following instances are running: ")
for idx, res in enumerate(reservations):
    print (idx, res.id, res.instances)

#Show instance details
for reservation in reservations:
    print ("---------------")
    print (reservation.instances[0].private_ip_address)
    print (reservation.instances[0].placement)

#Kill instance
#kill_instance_id = reservations[0].instances[0]
#api_conn.terminate_instances(instance_ids=[kill_instance_id])

# Create volume
vol_size = 30 # in GB
vol_region = 'melbourne-np'

vol_req = conn.create_volume(vol_size, vol_region)

#------------------

#Check provisioning status

curr_vol = api_conn.get_all_volumes([vol_req.id])[0]

print (curr_vol.status)

print (curr_vol.zone)

#Attach volume

api_conn.attach_volume (vol.id, inst.id, "/dev/vdc")
