import socket

class Sensor:
    def __init__(self, sensorType, session, port):
        self.sensorType = sensorType
        self.session = session
        self.port = port

    def generate_data(self, sensorType):
        print('Collecting/Generating Data for sensor type:', (sensorType))
        return None

    def send_data(self, data):
        print('Sending Data to Sync Node \n')
        return None
