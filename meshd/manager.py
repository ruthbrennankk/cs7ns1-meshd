from abc import abstractmethod
from uuid import UUID
import queue

class ClosableProtocolConnection:
    @abstractmethod
    def close(self):
        pass

# Primary Class Author : Chao, Secondary: Ruth, Anton
class ProtocolConnectionManager:
    # peers: dict[UUID, ClosableProtocolConnection]

    def __init__(self):
        self.peers = {}
        self.sensors_status = [False] * 9 # NUM_SENSORS
        self.sensor_q = queue.Queue(100) # queue of sensor interactions limited to last 100 sensor interactions.

    def __contains__(self, remote_session: UUID):
        return remote_session in self.peers

    def get_sensor_status(self, sensor_code):
        return self.sensors_status[int(sensor_code)]

    def set_sensor_status(self, sensor_code, value):
        self.sensors_status[int(sensor_code)] = value

    def get_sensor_interactions(self):
        return self.sensor_q.queue

    def register_connection(self, uuid: UUID, connection: ClosableProtocolConnection):
        # self.unregister_connection(uuid)
        if (not self.peers.__contains__(uuid)):
            self.peers[uuid] = connection
            print(self.peers)

    def unregister_connection(self, uuid: UUID):
        connection = self.peers.pop(uuid, None)
        if connection is not None:
            connection.close()

    def recieved_data(self, transport, alert_type, sensor_type, data):
        if (len(self.peers) != 0):
            print('Sending to Known Peers')
            fail_set = set()
            for p in self.peers:
                try:
                    connection = self.peers[p]
                    print('peer uuid ', p)
                    self.sensor_q.put(sensor_type)
                    transport.send_data(connection.sock, alert_type, sensor_type, data)
                except:
                    fail_set.add(p)
            for p in fail_set:
                self.unregister_connection(p)
                print('Removed Peer: ' + str(p))
            print('Sent to Known Peers' + ' \n')
        else:
            print('no peers to share with' + '\n')
