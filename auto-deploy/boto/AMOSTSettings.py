#!/usr/bin/env python3
'''
Settings enabling access to CCC team's NeCTAR account
'''

#----Customizable Info-------------------------------------------
SECS_TO_WAIT = 50

#Instance region and NeCTAR API address
API_ENDPOINT = 'nova.rc.nectar.org.au'
API_REGION = 'melbourne-qh2'
API_PORT = 8773

#NeCTAR account details
ACCESS_KEY_ID = '6eb1a58e6b204427b1bb6b10b3926bf4'
SECRET_ACCESS_KEY = '4554aa0701ba43a5aa2eba1dbe5947b2'

#Instance details
KEY = 'amost-1'
I_TYPE = 'm2.tiny'  #Use m2.medium before deploying
SEC_GROUP = ['SSH']
    #NeCTAR Ubuntu 16.04 LTS (Xenial) amd64 (pre-installed murano-agent)
IMAGE = 'ami-c163b887'

VOL_SIZE = 35 # in GB
VOL_ZONE = 'melbourne-qh2'
VOL_TYPE = 'melbourne'
#----------------------------------------------------------------
