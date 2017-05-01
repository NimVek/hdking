import struct
import binascii
import pprint


class HDKingPacket(object):
    def __init__(self):
        self.stateless = True
        self.opcode = 0
        self.buffer = None

    def encode(self):
        raise NotImplementedError("AbstractMethod")

    def decode(self):
        raise NotImplementedError("AbstractMethod")

    def __str__(self):
        return pprint.pformat({self.__class__.__name__: self.content()})

    def content(self):
        return self.buffer


class HDKingPacketDummy(HDKingPacket):
    def __init__(self):
        self.opcode = 0

    def encode(self):
        pass

    def decode(self):
        pass


class HDKingPacketLoginRequest(HDKingPacket):
    def __init__(self):
        self.opcode = 0x110
	self.username = 'admin'
	self.password = '12345'

    def decode(self):
        pass

    def encode(self):
        self.buffer = self.username + '\0' * (64 - len(self.username)) + self.password + '\0' * (65 - len(self.password))

    def content(self):
        return None

class HDKingPacketLoginResponse(HDKingPacket):
    def __init__(self):
        self.opcode = 0x111
	self.username = 'admin'
	self.password = '12345'

    def decode(self):
        pass

    def encode(self):
        self.buffer = self.username + '\0' * (64 - len(self.username)) + self.password + '\0' * (65 - len(self.password))

    def content(self):
        return None


class HDKingPacketKeepAliveRequest(HDKingPacket):
    def __init__(self):
        self.opcode = 0x112

    def decode(self):
        pass

    def encode(self):
        self.buffer = ''

    def content(self):
        return None


class HDKingPacketKeepAliveResponse(HDKingPacket):
    def __init__(self):
        self.opcode = 0x113

    def decode(self):
        pass

    def encode(self):
        self.buffer = ''

    def content(self):
        return None


class HDKingPacketFindDeviceRequest(HDKingPacket):
    def __init__(self):
        self.opcode = 0x116

    def decode(self):
        pass

    def encode(self):
        self.buffer = '\0' * 72


class HDKingPacketFindDeviceResponse(HDKingPacket):
    def __init__(self):
        self.opcode = 0x115

    def decode(self):
        print(len(self.buffer))
        self.uid = self.buffer.split('\0', 1)[0]

    def encode(self):
        self.buffer = self.uid + '\0' * (72 - len(self.uid))

    def content(self):
        return {'uid': self.uid}


class HDKingPacketVideoData(HDKingPacket):
    def __init__(self):
        self.opcode = 0x1


class HDKingPacketAudioData(HDKingPacket):
    def __init__(self):
        self.opcode = 0x2
