#!/usr/bin/env python3
'''
Settings enabling access to Abhi's NeCTAR account
'''

#----Customizable Info-------------------------------------------
SECS_TO_WAIT = 20

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
SEC_GROUP = ['SSH']
    #NeCTAR Ubuntu 16.04 LTS (Xenial) amd64 (pre-installed murano-agent)
IMAGE = 'ami-c163b887'

VOL_SIZE = 30 # in GB
VOL_ZONE = 'melbourne-np'
VOL_TYPE = 'melbourne'
#----------------------------------------------------------------
