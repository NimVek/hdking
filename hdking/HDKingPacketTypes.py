import struct
import binascii


class HDKingPacket(object):
    def __init__(self):
        self.stateless = True
        self.opcode = 0
        self.buffer = None

    def encode(self):
        raise NotImplementedError("AbstractMethod")

    def decode(self):
        raise NotImplementedError("AbstractMethod")


class HDKingPacketDummy(HDKingPacket):
    def __init__(self):
	self.opcode = 0

    def encode(self):
        pass

    def decode(self):
        pass

    def __str__(self):
        #        return binascii.hexlify(self.buffer) + '\n' + str(self.buffer)
        return ''


class HDKingPacketFindDeviceRequest(object):
    def __init__(self):
        self.opcode = 0x116

    def decode(self):
        pass

    def encode(self):
        self.buffer = '\0' * 72


class HDKingPacketFindDeviceResponse(object):
    def __init__(self):
        self.opcode = 0x115

    def decode(self):
        print(len(self.buffer))
        self.uid = self.buffer.split('\0', 1)[0]

    def encode(self):
        self.buffer = self.uid + '\0' * (72 - len(self.uid))

    def __str__(self):
        return 'FindDeviceResponse: UID = %s' % self.uid
