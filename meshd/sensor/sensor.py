import socket
import random
import struct

import sys
sys.path.insert(0, '/Users/ruthbrennan/Documents/5th_Year/cs7ns1-meshd/') # location of src
from meshd.utils.sign import hash_payload
from meshd.transport.transport import Transport

class Sensor:

    # generates intial params on start
    # randomly progresses 'vehicle' down path during each data collection cycle
    # generates other params randomly.

    def __init__(self, sensorType, session, port):
        self.sensorType = sensorType
        self.session = session
        self.port = port

        self.x_pos = random.randint(20,80)
        self.y_pos = random.randint(20,80)
        self.x_lim = 100
        self.y_lim = 100 # defined city block range for travel
        self.journey_len = random.randint(20,50)
        self.pressure = 35
        self.current_step = 0
        # Added by Mahislami
        self.fuel = 100
        self.speed = random.randint(10, 90)
        self.speed_lower_lim = 0
        self.speed_upper_lim = 90
        self.fuel_lim = 0
        self.wind = 0
        self.humidity = 0

    def generate_data(self, sensorType):
        metricMap = {'position': self.getPos(),
           'temperature': self.getTemp(),
           'tyre_pressure': self.getPressure(),
           'journey_elapsed': self.getElapsed(),
           'journey_finished': self.getStatus(),
           'journey_finished': self.getStatus(),
           'fuel': self.getFuel(),
           'speed': self.getSpeed(),
           'wind': self.getWind(),
           'humidity':self.getHumidity()
       }

        print('Collecting data from sensor type:', (sensorType))
        if sensorType not in metricMap:
            print('Invalid sensor type found')
            return None
        return metricMap.get(sensorType)

    def send_data(self, data):
        hostname = socket.gethostname()
        print("Hostname : " + socket.gethostbyname(hostname) + " Port : " + self.port)
        print('Sending Data to Sync Node \n')
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect_ex((socket.gethostbyname(hostname), int(self.port)))
        data = str(data)
        alert_type = 1  # update alert
        if self.sensorType == 'fuel' or self.sensorType == 'tyre_pressure' or self.sensorType == 'speed':
            alert_type = 2  # status alert
        if self.sensorType == 'temperature' or self.sensorType == 'humidity' or self.sensorType == 'wind':
            alert_type = 3  # environment alert
        if self.sensorType == 'journey_finished' or self.sensorType == 'journey_elapsed':
            alert_type = 4  # status alert

        Transport().send_data(sock, alert_type, data)
        sock.close()

    def getPressure(self):
        self.pressure = self.pressure - random.uniform(0, 0.5)
        return self.pressure

    def getTemp(self):
        return random.uniform(5, 35)

    def getPos(self):
        if self.current_step < self.journey_len:
            self.makeMove()
            self.current_step += 1
        return (self.x_pos, self.y_pos)

    def getElapsed(self):
        return self.current_step

    def getStatus(self):
        if self.current_step < self.journey_len:
            return False
        return True

    def makeMove(self):
        dir = random.randint(1, 2)  # x or y movement in given move
        move_len = random.randint(1, 3)
        disp = [-1, 1][random.randrange(2)] * move_len
        if dir == 1:
            self.y_pos += disp
        else:
            self.x_pos += disp
        self.reduceFuel(random.uniform(5, 10))
        self.limitFuel()
        self.limitPosition()

    def limitPosition(self): # stay in range
        if self.x_pos > self.x_lim:
            self.x_pos = self.x_lim
        if self.y_pos > self.y_lim:
            self.y_pos = self.y_lim
        if self.x_pos < 0:
            self.x_pos = 0
        if self.y_pos < 0:
            self.y_pos = 0

    def limitFuel(self):
        if self.fuel < self.fuel_lim:
            self.fuel = self.fuel_lim
            print("Vehicle out of Fuel!")

    def limitSpeed(self):
        if self.speed > self.speed_upper_lim:
            self.speed = self.speed_upper_lim
        if self.speed < self.speed_lower_lim:
            self.speed = self.speed_lower_lim

    def reduceFuel(self, amount):
        self.fuel = self.fuel - amount

    def getFuel(self):
        return self.fuel

    def getHumidity(self):
        return random.uniform(0, 100)

    def getWind(self):
        return random.uniform(0, 25)

    def getSpeed(self):
        self.speed = self.speed + random.uniform(-10, 10)
        return self.speed