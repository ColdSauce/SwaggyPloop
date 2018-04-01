#!/usr/bin/env python3

from data_decoder import Decoder
from data_encoder import Encoder

if __name__ == '__main__':
    with open('test_files/russel.txt', 'r') as f:
        file_contents = f.read()
        mac = '0A2B3C'
        timestamp = '1234567890'
        name = 'test'
        encoded = Encoder.encode_payload(mac, timestamp, name, file_contents)
        decoded = [Decoder.decode_request(request) for request in encoded]
        payloads = [decoded[3] for request in decoded]
        reconstructed_data = Decoder.reconstruct_data(payloads)
        print(reconstructed_data == file_contents)
