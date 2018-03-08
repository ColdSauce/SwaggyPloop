from data_decoder import Decoder
from data_encoder import Encoder

with open('test_files/russel.txt', 'r') as f:
    file_contents = f.read()
    mac = '0A2B3C'
    timestamp = '9999'
    name = 'universal'
    encoded = Encoder().encode(mac, timestamp, name, file_contents)
    decoded = Decoder().decode(encoded)
    print(Encoder().encode(mac, timestamp, name, decoded[3]) == encoded)
