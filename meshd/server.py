import socket
import struct
from utils import hash_payload

DISCOVERY_PORT = 0
SENSOR_PORT = 33211

class Protocol:
    def __init__(self, discovery_port=DISCOVERY_PORT):
        self.discovery_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.discovery_server.bind(('', discovery_port))
        self.discovery_server.listen()

        _, self.discovery_port = self.discovery_server.getsockname()
        self.peers = set()

    def update_peers_set(self, session, addr, port):
        '''
            Update our peer set based on discovery
        '''
        print('Discovered session %s from %s:%d' % (session, addr, port))
        new_peer = (addr, port)
        if (new_peer not in self.peers):
            self.peers.add(new_peer)
            print('Discovered session %s added to peers \n' % (session))
        else:
            print('Discovered session %s already a peer \n' % (session))

    def read_peer(self):
        '''
            Read protocol packets from the our peers
        '''
        return None

    def read_sensor(self):
        '''
            Read protocol packets from the our sensors
        '''
        return None

    def send_to_peers(self, data):
        fail_set = set()
        for p in self.peers:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
                sock.connect(p)
                # TODO - Prepare Data
                hash = hash_payload(data)
                packet = struct.pack('!32s%ds' % len(data), hash, data)
                sock.send(packet)
                sock.close()
            except:
                fail_set.add(p)
        for p in fail_set:
            self.peers.discard(p)
            print('Removed Peer: ', p)

    def close(self):
        self.discovery_server.close()
