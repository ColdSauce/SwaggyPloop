#!/usr/bin/env python3
# This module handles the encoding of a large data payload into multiple DNS
# requests.

import base64
import more_itertools

from constants import *

class Encoder():

    @staticmethod
    def __get_request_prefix__(mac_address, timestamp, sequence_number):
        """
        Validates and returns the DNS request prefix.
        """
        assert len(mac_address) == MAC_ADDRESS_BYTES
        assert len(timestamp) == TIMESTAMP_BYTES
        assert len(str(sequence_number)) <= SEQUENCE_NUMBER_BYTES
        padded_sequence_number = (
            '{:0' + str(SEQUENCE_NUMBER_BYTES) + 'd}').format(sequence_number)
        return str(mac_address) + str(timestamp) + padded_sequence_number

    @staticmethod
    def __split_payload__(payload):
        """
        Encodes the given payload with base64 and splits it into chunks of size
        PAYLOAD_BYTES.
        """
        payload_base64 = base64.b64encode(
            payload.encode('ascii')).decode('utf-8')
        return more_itertools.sliced(payload_base64, PAYLOAD_BYTES)

    @staticmethod
    def encode_payload(mac_address, timestamp, name, payload):
        """
        Given a MAC address, timestamp identifier, payload name, and the raw
        payload data, this function returns a list of formatted requests to send
        through DNS. Each packet consists of a formatted prefix containing the
        MAC address and timestamp identifier followed by a chunk of the payload.
        The first packet sent will contain the payload name and the last packet
        sent will contain an end delimeter.

        MAC address will be used to identify where the payload originated, and
        the timestamp identifier will be used to identify requests that are
        parts of a single payload. Each request carrying a part of a split
        payload will have the same timestamp identifier since it represents
        the creation time of the payload.
        """
        payloads = [name] + list(Encoder.__split_payload__(payload)) + ['\\E']
        requests = []
        for sequence_number, payload in enumerate(payloads):
            prefix = Encoder.__get_request_prefix__(
                mac_address, timestamp, sequence_number)
            request = prefix + payload
            requests.append(request)
        return requests

if __name__ == '__main__':
    print(Encoder.encode_payload('ABCDEF', '1111100000', 'bobthe', 'dasdf'))
