import socket
import struct

from sign import hash_payload
from sign import decode_alert
from sign import decode_sensor

class Transport:

    def send_data(self, sock, alert_type, sensor_type, data):
        print("Peer Data sending: " + data)

        data = str(data)
        payload = struct.pack('!16s', bytes(data, 'utf-8'))
        hash = hash_payload(payload)
        packet = struct.pack('!32s2i16s', hash, alert_type, sensor_type,  payload)
        sock.send(packet)
        print("Peer Data sent: " + data + " from sensor of type " + decode_sensor(sensor_type))

    def recieve_sensor_data(self, data):
        hash, alert_type, sensor_type, payload = struct.unpack('!32s2i16s', data)
        if hash != hash_payload(payload):
            print("Received packet of wrong hash from sensor")
            return None
        data = struct.unpack('!16s', payload)[0].decode()
        alert_str = decode_alert(alert_type)
        print("Sensor Data recieved: " + str(data) + " with alert_type = " + str(alert_str) + " from sensor_type =  " + str(decode_sensor(sensor_type)) + ' \n')
        return (alert_type, sensor_type,  data)
