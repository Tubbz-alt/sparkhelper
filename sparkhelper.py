"""

Copyright (c) 2018 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.0 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

"""
from __future__ import absolute_import, division, print_function

import datetime as dt
import requests
import json
import hashlib
import hmac

__author__ = "Tim Taylor <timtayl@cisco.com>"
__contributors__ = []
__copyright__ = "Copyright (c) 2018 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.0"


def membership_check(room_Id, bot_token, allowed_person_Org_Id):
    date_time = dt.datetime.now()
    print("{}, membership_check starting".format(date_time))
    the_url = 'https://api.ciscospark.com/v1/memberships?roomId={}'.format(room_Id)
    room_member_orgs_allowed = False

    get_request_headers = {"Authorization": "Bearer {}".format(bot_token)}

    message_response = requests.get(the_url, verify=True, headers=get_request_headers)
    if message_response.status_code == 200:

        message_json = json.loads(message_response.text)

        org_id_list = [d['personOrgId'] for d in message_json['items']]

        number_orgs_not_allowed = len(set(org_id_list).symmetric_difference(allowed_person_Org_Id))
        print('{}:   membership_check: items not in allowed or list: {}'.format(date_time, number_orgs_not_allowed))

        if number_orgs_not_allowed == 0:
            room_member_orgs_allowed = True
    else:
        print("{},   membership check failed: {}".format(date_time, message_response))

    print("{}, membership_check ending".format(date_time))
    return room_member_orgs_allowed


def verify_signature(key, raw_request_data, request_headers):
    date_time = dt.datetime.now()
    print("{}: verify_signature: start".format(date_time))
    signature_verified = False
    # Let's create the SHA1 signature
    # based on the request body JSON (raw) and our passphrase (key)
    hashed = hmac.new(key, raw_request_data, hashlib.sha1)
    validated_signature = hashed.hexdigest()

    if validated_signature == request_headers.get('X-Spark-Signature'):
        signature_verified = True
        print("{}:   verify_signature: webhook signature is valid".format(dt.datetime.now()))
    else:
        print("{}.   verify_signature: webhook signature is NOT valid".format(dt.datetime.now()))

    print("{}: verify_signature: end".format(date_time))
    return signature_verified