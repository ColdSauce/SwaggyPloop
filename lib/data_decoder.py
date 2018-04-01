#!/usr/bin/env python3
# This module will be used to handle the decoding of encoded requests sent
# through DNS. This decoder will only split the requests into its appropriate
# segments and will not handle payload reconstruction.

import base64

from constants import *

MAC_ADDRESS = 0
TIMESTAMP = 1
SEQUENCE_NUMBER = 2
PAYLOAD = 3

class Decoder():

    @staticmethod
    def decode_request(request):
        prefix = request[:PREFIX_BYTES]
        mac_address = prefix[:MAC_ADDRESS_BYTES]
        prefix = prefix[MAC_ADDRESS_BYTES:]
        timestamp = prefix[:TIMESTAMP_BYTES]
        sequence_number = prefix[TIMESTAMP_BYTES:]
        payload = request[PREFIX_BYTES:]
        return mac_address, timestamp, sequence_number, payload

    @staticmethod
    def reconstruct_data(requests):
        mac_address = requests[0][MAC_ADDRESS]
        timestamp = requests[0][TIMESTAMP]
        name = requests[0][PAYLOAD]
        ordered = sorted(
            requests, key=lambda request: int(request[SEQUENCE_NUMBER]))
        payload = ''.join([request[PAYLOAD] for request in ordered[1:-1]])
        decoded_payload = base64.b64decode(
            payload.encode('ascii')).decode('utf-8')
        return mac_address, timestamp, name, decoded_payload
