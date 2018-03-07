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

    def _pack_data_segment(self, uuid, name, sequence_number, data):
        return uuid + name + '.' + self._pad_sequence_number(sequence_number) + data

    def encode(self, uuid, name, data):
        largest_a_dns_packet_can_be = 254
        uuid_bytes = 4
        sequence_number_bytes = 4
        header_bytes = uuid_bytes + len(name)
        amount_packets = int(len(data) / (largest_a_dns_packet_can_be - header_bytes)) + 1
        if amount_packets == 1:
            return [self._pack_data_segment(uuid, name, 0, data)]

        split_data = self._split_string_into_n_sequences(data, amount_packets)
        packed_data = [self._pack_data_segment(uuid, name, index, packet) for index, packet in enumerate(split_data)]
        return packed_data

print(Encoder().encode("hell", "yolo", "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"))
