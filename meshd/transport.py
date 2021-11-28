import socket
import struct

from sign import hash_payload
from sign import decode_alert

class Transport:

    def send_data(self, sock, alert_type, data):
        print("Peer Data sending: " + data)

        data = str(data)
        payload = struct.pack('!16s', bytes(data, 'utf-8'))
        hash = hash_payload(payload)
        packet = struct.pack('!32si16s', hash, alert_type, payload)
        sock.send(packet)

        print("Peer Data sent: " + data)

    def recieve_sensor_data(self, data):
        hash, alert_type, payload = struct.unpack('!32si16s', data)
        if hash != hash_payload(payload):
            print("Received packet of wrong hash from sensor")
            return None
        data = struct.unpack('!16s', payload)[0].decode()
        alert_str = decode_alert(alert_type)
        print("Sensor Data recieved: " + str(data) + " with alert_type = " + str(alert_str) + ' \n')
        return (alert_type, data)
