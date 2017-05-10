
#/////!/usr/bin/env python3

"""
Boto script to provision an instance on NeCTAR Research Cloud
@author: Abhi
S1, 2017
"""
import time
import boto
from boto.ec2.regioninfo import RegionInfo

#-----------CHANGE THIS TO CORRECT SETTINGS FILE--------------
import AMOSTSettings as info
#-------------------------------------------------------------

#----Customize Info-------------------------------------------
SECS_TO_WAIT = info.SECS_TO_WAIT

#Instance region and NeCTAR API address
API_ENDPOINT = info.API_ENDPOINT
API_REGION = info.API_REGION
API_PORT = info.API_PORT

#NeCTAR account details
ACCESS_KEY_ID = info.ACCESS_KEY_ID
SECRET_ACCESS_KEY = info.SECRET_ACCESS_KEY

#Instance details
KEY = info.KEY
I_TYPE = info.I_TYPE
SEC_GROUP = info.SEC_GROUP
    #NeCTAR Ubuntu 16.04 LTS (Xenial) amd64 (pre-installed murano-agent)
IMAGE = info.IMAGE

VOL_SIZE = info.VOL_SIZE # in GB
VOL_ZONE = info.VOL_ZONE
VOL_TYPE = info.VOL_TYPE
#-------------------------------------------------------------

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
    Prints ab infoout each instance running on the account
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

def print_instance_info(res):
    """
    Prints out basic info of the first instance in a reservation
    """
    print()
    print("New instance created with the following details:")
    print("Private IP: ", res.instances[0].private_ip_address)
    print("Zone: ", res.instances[0].placement)
    print("ID: ", res.instances[0].id)
    print("Key: ", res.instances[0].key_name)
    print()

def create_instance(api_connection):
    """
    Creates an instance on the cloud
    """
    return api_connection.run_instances(
        IMAGE,
        key_name=KEY,
        instance_type=I_TYPE,
        security_groups=SEC_GROUP,
        placement=API_REGION)

def kill_instance(api_connection, instance_id):
    """
    Kill instance
    """
    api_connection.terminate_instances(instance_ids=[instance_id])

def update_res_info(api_connection, old_res):
    """
    Updates the reservation info as the old one...
    ...may not have all details e.g. IP and Zone
    """
    reservations = api_connection.get_all_reservations()
    for res in reservations:
        if res.id == old_res.id:
            return res

def print_vol_info(api_connection):
    """
    Prints info on all volumes
    """
    volumes = api_connection.get_all_volumes()
    for volume in volumes:
        print(volume.status)
        print(volume.zone)



def main():
    """
    Main func
    """

    # Establish connection to API gateway
    api_conn = connect_to_api()
    print("Connected to NeCTAR API")

    # Create a new instance; contains res.id
    new_reservation = create_instance(api_conn)
    print("Instance launched.")

    #Create a volume
    vol_req = api_conn.create_volume(
        VOL_SIZE, VOL_ZONE, volume_type=VOL_TYPE)
    print(
        "Volume", vol_req.id, "of size", vol_req.size,
        "GB created in", vol_req.zone)

    #wait for some time while instance & vol initialize
    print("Waiting for the dust to settle...")
    time.sleep(SECS_TO_WAIT)

    #get & print current reservation's info
    res = update_res_info(api_conn, new_reservation)
    print_instance_info(res)

    #Attach volume; path doesn't seem to work - NeCTAR doesn't care
    if api_conn.attach_volume(vol_req.id, res.instances[0].id, "/dev/vdb"):
        print("Volume attached successfully.")

if __name__ == '__main__':
    main()
