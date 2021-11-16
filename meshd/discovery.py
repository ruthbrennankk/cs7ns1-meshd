import hashlib
import socket
import struct
from threading import Thread
from time import sleep
from uuid import UUID

MCAST_GROUP = '224.1.1.1'
MCAST_PORT = 33210
MCAST_TTL = 2

SHARED_KEY = b'meshd'


class Discovery:
    def __init__(self, protocol_port: int, session: UUID, mcast_group=MCAST_GROUP, mcast_port=MCAST_PORT):
        self.protocol_port = protocol_port
        self.session = session

        self.group = mcast_group
        self.port = mcast_port

        self.sock = self.create_socket(mcast_group, mcast_port)

    def close(self):
        self.sock.close()

    def create_socket(cls, group, port):
        # create udp socket
        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM,
            socket.IPPROTO_UDP,
        )
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MCAST_TTL)
        sock.bind(('', port))

        # join multicast group
        mreq = struct.pack('=4sl', socket.inet_aton(group), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        return sock

    def hash_payload(cls, payload):
        """
        Calculate the hash of the payload using the shared key.
        """
        m = hashlib.sha256()
        m.update(payload + SHARED_KEY)
        return m.digest()

    def read(self):
        len_packet = 32 + 16 + 2  # 32 bytes hash, 16 bytes session, 2 bytes port

        # verify packet length
        bytes, (remote_addr, remote_port) = self.sock.recvfrom(len_packet)
        if (len_packet != len(bytes)):
            print('Received packet of wrong size %d from %s:%d' % (len(bytes), remote_addr, remote_port))
            return None

        # verify payload hash against shared key
        hash, payload = struct.unpack('!32s%ds' % (len(bytes) - 32), bytes)
        if hash != self.hash_payload(payload):
            print('Received packet of wrong hash from %s:%d' % (remote_addr, remote_port))
            return None

        # decode payload
        _, session, protocol_port = struct.unpack('!32s16sH', bytes)
        session = UUID(bytes=session)

        return session, (remote_addr, protocol_port)

    def send(self):
        # encode payload and hash
        payload = struct.pack('!16sH', self.session.bytes, self.protocol_port)
        hash = self.hash_payload(payload)

        # construct and send packet
        packet = struct.pack('!32s%ds' % len(payload), hash, payload)
        self.sock.sendto(packet, (self.group, self.port))
