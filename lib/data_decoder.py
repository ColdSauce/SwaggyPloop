#!/usr/bin/env python3
# This module will be used to handle the decoding of encoded requests sent
# through DNS.

import base64
import os
import sys

# Constants
FILEPATH = os.path.abspath(__file__)
MAC_ADDRESS = 0
TIMESTAMP = 1
SEQUENCE_NUMBER = 2
PAYLOAD = 3

# Path modification for project dependencies
def parent_chain(path, n):
    for i in range(n):
        path = os.path.dirname(path)
    return path
sys.path.insert(1, parent_chain(FILEPATH, 2))

# Project level dependencies
from lib.constants import *

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
    def reconstruct_data(payloads):
        """
        Given a list of encoded payloads (assumed to be ordered correctly),
        this function reconstructs the original data by combining and base64
        decoding the payloads.
        """
        combined_payload = ''.join(payloads)
        print(combined_payload)
        decoded_payload = base64.b64decode(
            combined_payload.encode('ascii')).decode('utf-8')
        return decoded_payload
