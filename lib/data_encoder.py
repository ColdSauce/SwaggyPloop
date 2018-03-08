#!/usr/bin/env python3

class Encoder():
    def _split_string_into_n_sequences(self, s, n):
        split_at = int(len(s) / n)
        result_list = []
        for index in range(0, len(s), split_at):
            if index > len(s) - split_at - 1:
                result_list.append(s[index:])
            else:
                result_list.append(s[index:index + split_at])

        return result_list

    def _pad_sequence_number(self, num):
        padded = ""
        sequence_number_bytes = 4
        amount_needed_to_pad =  sequence_number_bytes - len(str(num))
        for r in range(0, amount_needed_to_pad):
            padded += "0"

        return padded + str(num)

    def _pack_data_segment(self, mac_address, timestamp, name, sequence_number, data, is_last_packet):
        to_return =  mac_address + timestamp + name + '.' + self._pad_sequence_number(sequence_number) + data
        if is_last_packet:
            to_return += '\\E'
        return to_return

    def _get_header_bytes(self):
        mac_address_bytes = 6
        timestamp_bytes = 4
        delimiter_byte = 1
        sequence_number_bytes = 4
        end_bytes = 2
        return mac_address_bytes + timestamp_bytes + sequence_number_bytes + end_bytes + delimiter_byte

    def encode(self, mac_address, timestamp, name, data):
        largest_a_dns_packet_can_be = 254
        
        header_bytes = self._get_header_bytes()
        amount_packets = int(len(data) / (largest_a_dns_packet_can_be - header_bytes)) + 1
        is_last_packet = False
        if amount_packets == 1:
            is_last_packet = True
            return [self._pack_data_segment(mac_address, timestamp, name, 0, data, is_last_packet)]

        split_data = self._split_string_into_n_sequences(data, amount_packets)

        packed_data = []
        for index, packet in enumerate(split_data):
            if index == len(split_data) - 1:
                is_last_packet = True
            packed_data.append(self._pack_data_segment(mac_address, timestamp, name, index, split_data[index], is_last_packet))
        return packed_data
