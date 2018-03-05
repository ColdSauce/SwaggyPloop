import socket

class DNSQuery:
    def __init__(self, data):
        self.data = data
        self.domain = ''

        type = (ord(data[2]) >> 3) & 15   # Opcode bits
        if type == 0:                     # Standard query
            ini = 12
            lon = ord(data[ini])
            while lon != 0:
                self.domain+=data[ini+1:ini+lon+1]+'.'
                ini+=lon+1
                lon=ord(data[ini])
        print(self.domain)
        print(len(self.domain))

    def response(self, ip):
        packet=''
        if self.domain:
            packet+=self.data[:2] + "\x81\x80"
            # Questions and Answers Counts
            packet+=self.data[4:6] + self.data[4:6] + '\x00\x00\x00\x00'
            # Original Domain Name Question
            packet+=self.data[12:]
            # Pointer to domain name
            packet+='\xc0\x0c'
            # Response type, ttl and resource data length -> 4 bytes
            packet+='\x00\x01\x00\x01\x00\x00\x00\x3c\x00\x04'
            # 4bytes of IP
            d = "".join(map(lambda x: chr(int(x)), ip.split('.')))
            packet += 'fuck'
            # print(repr(packet))
        return packet

if __name__ == '__main__':
    ip='112.34.23.23'
    udps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udps.bind(('0.0.0.0',53))

    try:
        while 1:
            data, addr = udps.recvfrom(1024)
            print(len(data))
            p = DNSQuery(data)
            udps.sendto(p.response(ip), addr)
    except KeyboardInterrupt:
        udps.close()
