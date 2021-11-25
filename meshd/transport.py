import socket

class Transport:
    def __init__(self, protocol):
        self.peers = set()
        self.host = socket.gethostbyname(socket.gethostname())
        self.protocol = protocol

    def update_peers_map(self, session, addr, port, own_protocol_port):
        '''
            Update our peer set based on discovery
        '''
        # print('Discovered session %s from %s:%d' % (session, addr, port))
        new_peer = (addr, port)
        if (new_peer != (self.host, own_protocol_port) and new_peer not in self.peers):
            self.peers.add(new_peer)
            print('Discovered session %s added to peers (%s:%d) \n' % (session, addr, port))
            print('New Peer List \n', self.peers)

    def read_peer(self):
        '''
            Read protocol packets from the our peers
        '''
        conn, addr = self.protocol.server.accept()
        data = conn.recv(1024)
        data = data.decode('utf-8')
        print(data + ' \n')
        conn.close()
        return data

    def read_sensor(self):
        '''
            Read protocol packets from the our sensors
        '''
        data = 'sensor data'
        self.send_to_peers(data)
        return None

    def send_to_peers(self, data):
        fail_set = set()
        for p in self.peers:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
                print('sending to peer ...', p)
                sock.connect(p)
                sock.send(data.encode())
                sock.close()
            except:
                fail_set.add(p)
        for p in fail_set:
            self.peers.discard(p)
            print('Removed Peer: ', p)

    def close(self):
        self.sock.close()
