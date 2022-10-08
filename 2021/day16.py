from functools import reduce


packetTypeMap = dict()


class Packet:

    def __init__(self, message: str):
        self.version = int(message[:3], 2)
        self.typeId = int(message[3:6], 2)
        self.length = 6

    def __repr__(self):
        return f"[v{self.version} typeId={self.typeId}]"

    def sumVersionNumbers(self):
        return self.version

    def eval(self):
        raise NotImplementedError()

    @classmethod
    def buildPacket(cls, message: str):
        typeId = int(message[3:6], 2)
        packetType = packetTypeMap.get(typeId) or packetTypeMap[None]
        packet = packetType(message)
        return packet


class LiteralPacket(Packet):

    def __init__(self, message: str):
        super().__init__(message)
        message = message[self.length:]

        literal, offset = '', 0
        while message[offset] == '1':
            literal += message[offset+1:offset+5]
            offset += 5
        literal += message[offset+1:offset+5]
        self.value = int(literal, 2)
        self.length += offset + 5

    def eval(self):
        return self.value


class OperatorPacket(Packet):

    def __init__(self, message: str):
        super().__init__(message)
        message = message[self.length:]

        self.packets = list()
        lengthType = message[0]
        lengthBits = 11 if '1' == lengthType else 15
        length = int(message[1:1+lengthBits], 2)
        self.length += 1 + lengthBits
        message = message[1+lengthBits:]
        if '0' == lengthType:
            # Length is bit length
            self.length += length
            message = message[:length]
            while len(message) > 6:
                packet = Packet.buildPacket(message)
                self.packets.append(packet)
                message = message[packet.length:]
        else:
            # Length is total packet count
            for _ in range(length):
                packet = Packet.buildPacket(message)
                self.packets.append(packet)
                message = message[packet.length:]
                self.length += packet.length

    def sumVersionNumbers(self):
        return self.version + sum(a.sumVersionNumbers() for a in self.packets)

    def eval(self):
        if self.typeId == 0:
            return sum(a.eval() for a in self.packets)
        if self.typeId == 1:
            return reduce(lambda a, b: a*b, list(a.eval() for a in self.packets))
        if self.typeId == 2:
            return min(a.eval() for a in self.packets)
        if self.typeId == 3:
            return max(a.eval() for a in self.packets)
        if self.typeId == 5:
            return 1 if self.packets[0].eval() > self.packets[1].eval() else 0
        if self.typeId == 6:
            return 1 if self.packets[0].eval() < self.packets[1].eval() else 0
        if self.typeId == 7:
            return 1 if self.packets[0].eval() == self.packets[1].eval() else 0
        raise RuntimeError(f"Unknown typeId={self.typeId}")


packetTypeMap[4] = LiteralPacket
packetTypeMap[None] = OperatorPacket

with open('day16.txt') as reader:
    for message in reader.readlines():
        message = message.strip()
        print(f"### Processing  message '{message}'")
        messageBin = ''.join(list(
            str(bin(int(message[i: i+2], 16)))[2:].zfill(8)
            for i in range(0, len(message), 2)
        ))
        packet = Packet.buildPacket(messageBin)
        testLen = (packet.length // 8)*8 + (8 if (packet.length % 8) else 0)
        print(packet.eval())

print(f"done")
