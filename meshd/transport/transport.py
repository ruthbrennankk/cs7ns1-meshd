import socket
import struct
import sys
# sys.path.insert(0,'/users/ugrad/brennar5/ruth/cs7ns1-meshd/')
sys.path.insert(0,'/Users/ruthbrennan/Documents/5th_Year/cs7ns1-meshd/')

from meshd.utils.sign import hash_payload
from meshd.utils.sign import decode_alert
from meshd.utils.sign import decode_sensor

class Transport:

    def send_data(self, sock, alert_type, sensor_type, data):
        print("Peer Data sending: " + data)

        data = str(data)
        payload = struct.pack('!16s', bytes(data, 'utf-8'))
        hash = hash_payload(payload)
        packet = struct.pack('!32s2i16s', hash, alert_type, sensor_type,  payload)
        sock.send(packet)

        print("Peer Data sent: " + data + " from sensor of type " + decode_sensor(sensor_type))

    def recieve_sensor_data(self, data, peer):
        hash, alert_type, sensor_type, payload = struct.unpack('!32s2i16s', data)
        if hash != hash_payload(payload):
            print("Received packet of wrong hash from sensor")
            return None
        data = struct.unpack('!16s', payload)[0].decode()
        alert_str = decode_alert(alert_type)
        sensor_str = decode_sensor(sensor_type)
        if (peer):
            print(f'Recieved a peer data alert: {alert_str} Sensor type : {sensor_str} message: {data} \n')
            # print("Peer Data recieved: " + str(data) + " with alert_type = " + str(alert_type) + ' \n')
        else:
            print("Sensor Data recieved: " + str(data) + " with alert_type = " + str(alert_str) + " from sensor_type =  " + str(decode_sensor(sensor_type)) + ' \n')
        return (alert_type, sensor_type, data)
