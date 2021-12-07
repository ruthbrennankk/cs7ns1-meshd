import socket
import struct
from threading import Event, Thread
from uuid import UUID
from sign import hash_payload
from manager import ProtocolConnectionManager
from transport import Transport

READ_TIMEOUT = 1

# Primary Class Author : Chao, Secondary: Ruth
class InvalidRemoteHelloError(Exception):
    def __init__(self, reason):
        super().__init__(reason)
        self.reason = reason

class ProtocolConnection:
    def __init__(self, incoming: bool, local_session: UUID, sock: socket.socket, manager: ProtocolConnectionManager, read_timeout=READ_TIMEOUT):
        self.incoming = incoming
        self.local_session = local_session
        self.read_timeout = read_timeout
        self.manager = manager
        self.sock = sock

    @staticmethod
    def accept(local_session, sock, manager, stop_event: Event):
        Thread(target=ProtocolConnection(True, local_session, sock, manager).run, args=(stop_event,)).start()

    @staticmethod
    def connect(local_session, remote_addr, remote_port, manager, stop_event: Event):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((remote_addr, remote_port))
        connection = ProtocolConnection(False, local_session, sock, manager)
        Thread(target=connection.run, args=(stop_event,)).start()
        return connection

    def close(self):
        pass

    def run(self, stop_event: Event):
        remote_addr, remote_port = self.sock.getpeername()
        remote_session = None

        try:
            local_hello = struct.pack('!32s16s', hash_payload(self.local_session.bytes), self.local_session.bytes)
            self.sock.send(local_hello)

            self.sock.setblocking(False)
            self.sock.settimeout(self.read_timeout)

            remote_hello = self.sock.recv(16 + 32)
            remote_hello_sign, remote_hello = struct.unpack('!32s16s', remote_hello)
            if remote_hello_sign != hash_payload(remote_hello):
                raise InvalidRemoteHelloError('Invalid remote payload signature')
            remote_session = UUID(bytes=remote_hello)

            if self.incoming and self.local_session.int >= remote_session.int:
                raise InvalidRemoteHelloError('Unexpected incoming connection with lower session id')
            if not self.incoming and self.local_session.int <= remote_session.int:
                raise InvalidRemoteHelloError('Unexpected outgoing session with higher session id')

            if self.incoming:
                print(f'Accepted incoming connection from {remote_session} at {remote_addr}:{remote_port}')
            else:
                print(f'Connected to {remote_session} at {remote_addr}:{remote_port}')

            self.manager.register_connection(remote_session, self)

            while not stop_event.is_set():
                try:
                    res = self.sock.recv(1024)
                    if(res):
                        # (alert_type, data) = Transport().recieve_sensor_data(res, True)
                        Transport().recieve_sensor_data(res, True)
                        # print(f'Recieved a peer data alert: {alert_type} message: {data} \n')
                        # Thread(target=self.manager.recieved_data, args=(Transport(), alert_type, data)).start()
                except socket.timeout:
                    pass

        except socket.error as e:
            if remote_session is None:
                print(f'Socket error at {remote_addr}:{remote_port}: {e}')
            else:
                print(f'Socket error with {remote_session} at {remote_addr}:{remote_port}: {e}')
        finally:
            self.sock.close()
