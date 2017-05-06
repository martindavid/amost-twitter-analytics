#!/usr/bin/env python3

"""
Boto script to provision an instance on NeCTAR Research Cloud
@author: abhi
S1, 2017
"""

import boto
from boto.ec2.regioninfo import RegionInfo

#----Customizable Info-------------------------------------------
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
    #NeCTAR Ubuntu 16.04 LTS (Xenial) amd64 (pre-installed murano-agent)
IMAGE = 'ami-c163b887'

VOL_SIZE = 30 # in GB
VOL_REGION = 'melbourne-np'
#----------------------------------------------------------------

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

def print_current_instances(api_connection):
    """
    Prints info about each instance running on the account
    """
    reservations = api_connection.get_all_reservations()

    #Show reservation details
    print("The following instances are running: ")
    for idx, res in enumerate(reservations):
        print(idx, res.id, res.instances)

    #Show instance details
    for idx, reservation in enumerate(reservations, 1):
        print(idx, "---------------")
        print("IP: ", reservation.instances[0].private_ip_address)
        print("Zone: ", reservation.instances[0].placement)

def create_instance(api_connection, image, key, i_type, sec_group):
    """
    Creates an instance on the cloud
    """
    return api_connection.run_instances(
        image,
        key_name=key,
        instance_type=i_type,
        security_groups=sec_group)

def kill_instance(api_connection, instance_id):
    """
    Kill instance
    """
    api_connection.terminate_instances(instance_ids=[instance_id])

def update_res_info(api_connection, old_res):
    reservations = api_connection.get_all_reservations()
    for res in reservations:
        if res.id == old_res.id:
            return res

def print_vol_info(api_connection, volume_request):
    """
    Prints info on all volumes
    """
    volumes = api_connection.get_all_volumes([volume_request.id])[0]
    for volume in volumes:
        print(volume.status)
        print(volume.zone)

def attach_volume(api_connection, volume_id, instance_id, path):
    """
    Attach volume
    """
    return api_connection.attach_volume(volume_id, instance_id, path)

def main():
    """
    Main func
    """
    # Establish connection to API gateway
    api_conn = connect_to_api()

    # Create a new instance; contains res.id
    new_reservation = create_instance(api_conn, IMAGE, KEY, I_TYPE, SEC_GROUP)
    print("New instance created.")

    #wait for some time while the new instance gets its IP addr
    #???

    #get current reservation's info
    res = update_res_info(api_conn, new_reservation)

    #print new instance's info
    print("IP: ", res.instances[0].private_ip_address)
    print("Zone: ", res.instances[0].placement)

    #Create a volume
    vol_req = api_conn.create_volume(VOL_SIZE, VOL_REGION)

    #Print info on all volumes
    print_vol_info(api_conn, vol_req)

    #Attach volume
    #if (attach_volume(api_conn, vol.id, inst.id, "/dev/vdc")):
    #   print("Volume attached successfully.")


if __name__ == '__main__':
    main()
