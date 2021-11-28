import socket
import struct
import sys
# sys.path.insert(0,'/users/ugrad/brennar5/ruth/cs7ns1-meshd/')
sys.path.insert(0,'/Users/ruthbrennan/Documents/5th_Year/cs7ns1-meshd/')

from meshd.utils.sign import hash_payload

class Transport:

    def send_data(self, sock, alert_type, data):
        print("Peer Data sending: " + data)

        data = str(data)
        payload = struct.pack('!16s', bytes(data, 'utf-8'))
        hash = hash_payload(payload)
        packet = struct.pack('!32si16s', hash, alert_type, payload)
        sock.send(packet)

        print("Peer Data sent: " + data)

    def recieve_sensor_data(self, data, peer):
        hash, alert_type, payload = struct.unpack('!32si16s', data)
        if hash != hash_payload(payload):
            print("Received packet of wrong hash from sensor")
            return None
        data = struct.unpack('!16s', payload)[0].decode()
        if (peer):
            print("Peer Data recieved: " + str(data) + " with alert_type = " + str(alert_type) + ' \n')
        else:
            print("Sensor Data recieved: " + str(data) + " with alert_type = " + str(alert_type) + ' \n')
        return (alert_type, data)
