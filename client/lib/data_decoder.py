class Decoder():
    def _unpad_sequence_number(self, num):
        return int(num)

    def _unpack_data_segment(self, data):
        uuid_bytes = 4
        sequence_number_bytes = 4

        uuid = data[:uuid_bytes]
        data = data[uuid_bytes:]

        name = data[:data.find('.')]
        data = data[data.find('.'):]

        sequence_number = self._unpad_sequence_number(data[1:sequence_number_bytes + 1])
        data = data[sequence_number_bytes + 1:]

        final_unpacked_data = data

        return (uuid, name, sequence_number, final_unpacked_data)


    def decoder(self, packets):
        decoded_packets = [self._unpack_data_segment(data_segment) for data_segment in packets]
        return decoded_packets
