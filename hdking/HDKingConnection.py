from .HDKingShared import *
from .HDKingPacketTypes import *

import struct
import sys


class HDKingConnection(object):
    def __iter__(self):
        return self

    def next(self):
        packet = self.receive()
        if not packet:
            raise StopIteration
        return packet


class HDKingStatelessConnection(HDKingConnection):
    def __init__(self, rfile, wfile):
        self.__prefix = 0xabcd
        self.__packages = {
            0x110: HDKingPacketLoginRequest,
            0x111: HDKingPacketLoginResponse,
            0x112: HDKingPacketKeepAliveRequest,
            0x113: HDKingPacketKeepAliveResponse,
            0x115: HDKingPacketFindDeviceResponse,
            0x116: HDKingPacketFindDeviceRequest,
        }
        self.__rfile = rfile
        self.__wfile = wfile

    def receive(self):
        header = self.__rfile.read(8)
        if len(header) != 8:
            return None
        prefix, size, opcode = struct.unpack('!HHL', header)
        log.debug("Receive packet: opcode = %s, size %d" % (hex(opcode), size))
        buffer = self.__rfile.read(size)
        if len(buffer) != size:
            return None
        if opcode in self.__packages:
            packet = self.__packages[opcode]()
        else:
            packet = HDKingPacketDummy()
        packet.buffer = buffer
        packet.decode()
        return packet

    def send(self, packet):
        packet.encode()
        header = struct.pack('!HHL', self.__prefix, len(packet.buffer),
                             packet.opcode)
        self.__wfile.write(header + packet.buffer)


class HDKingStatefulConnection(HDKingConnection):
    def __init__(self, rfile, wfile):
        self.__prefix = 0xbcde
        self.__packages = {}
        self.__rfile = rfile
        self.__wfile = wfile

    def receive(self):
        header = self.__rfile.read(8)
        if len(header) != 8:
            return None
        prefix, size, seq_nr, opcode = struct.unpack('!HHHH', header)
        log.debug("Receive packet: opcode = %s, size %d" % (hex(opcode), size))
        buffer = self.__rfile.read(size)
        if len(buffer) != size:
            return None
        if opcode in self.__packages:
            packet = self.__packages[opcode]()
        else:
            packet = HDKingPacketDummy()
            packet.opcode = opcode
        packet.buffer = buffer
        packet.decode()
        return packet

    def send(self, packet):
        packet.encode()
        header = struct.pack('!HHL', self.__prefix, len(packet.buffer),
                             packet.opcode)
        self.__wfile.write(header + packet.buffer)
