#!/usr/bin/env python3

class Packet():
    def __init__(self, mac_address, timestamp, name, sequence_number, data, is_last_packet):
        self.mac_address = mac_address
        self.timestamp = timestamp
        self.name = name
        self.sequence_number = sequence_number
        self.data = data
        self.is_last_packet = is_last_packet

    def __repr__(self):
        return str((self.mac_address, self.timestamp, self.name, self.sequence_number, self.data, self.is_last_packet))

    def __str__(self):
        return self.__repr__()

class Decoder():
    def get_packet_from_raw_data(self, data):
        mac_address_bytes = 6
        timestamp_bytes = 4
        sequence_number_bytes = 4

        # _read_packet does not mutate the string, so we need to take the
        # truncated data for passing to the next function
        mac_address, data = self._read_packet(mac_address_bytes, data)
        timestamp, data = self._read_packet(timestamp_bytes, data)
        name, data = self._read_packet(data.find('.'), data)
        sequence_number, data = self._read_packet(
            sequence_number_bytes, data, 1)
        sequence_number = self._unpad_sequence_number(sequence_number)

        is_last_packet = data.find('\\E') != -1
        if is_last_packet:
            # This removes the \\E delimiter
            data = data[:-2]

        final_unpacked_data = data

        return Packet(mac_address, timestamp, name, sequence_number, final_unpacked_data, is_last_packet)

    def _read_packet(self, bytes, packet, offset=0):
        data = packet[offset:bytes + offset]
        rest_of = packet[bytes + offset:]
        return (data, rest_of)

    def _unpad_sequence_number(self, num):
        return int(num)

    def _get_last_packet(self, packets):
        return list(filter(lambda packet: packet.is_last_packet, packets))[0]

    def _reconstruct_data(self, packets):
        last_packet = self._get_last_packet(packets)
        total_segments = last_packet.sequence_number
        resulting_list = []
        for l in range(0, last_packet.sequence_number + 1):
            resulting_list.append(None)
        for packet in packets:
            resulting_list[packet.sequence_number] = packet.data
        final_string = ''.join(resulting_list)
        return (last_packet.mac_address, last_packet.timestamp, last_packet.name, final_string)

    def decode(self, packets):
        decoded_packets = [
            self.get_packet_from_raw_data(data_segment)
            for data_segment in packets]
        return self._reconstruct_data(decoded_packets)
