import hashlib

SHARED_KEY = b'meshd-tester'

def hash_payload(payload):
    """
    Calculate the hash of the payload using the shared key.
    """
    m = hashlib.sha256()
    m.update(payload + SHARED_KEY)
    return m.digest()

# symmetrical map for encoding packet values
sensorTypeMap = {
    0:"position",
    1:"temperature",
    2:"tyre_pressure",
    3:"journey_elapsed",
    4:"journey_finished",
    5:"fuel",
    6:"speed",
    7:"packet_id",
    8:"humidity",

    "position":0,
    "temperature":1,
    "tyre_pressure":2,
    "journey_elapsed":3,
    "journey_finished":4,
    "fuel":5,
    "speed":6,
    "packet_id":7,
    "humidity":8
}

alertMap = {
    1: "update",
    2: "vehicle_status",
    3: "environment",
    4: "journey_status"
}

def decode_alert(alert_type):
    """
    Returns alert string for correspoding code.
    """
    return alertMap[alert_type]

def decode_sensor(sensor_type):
    """
    Returns sensor_type for correspoding packet code.
    """
    return sensorTypeMap[sensor_type]

