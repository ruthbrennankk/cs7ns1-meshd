import hashlib

SHARED_KEY = b'meshd-wip-proto-conn-2'

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

def hash_payload(payload):
    """
    Calculate the hash of the payload using the shared key.
    """
    m = hashlib.sha256()
    m.update(payload + SHARED_KEY)
    return m.digest()

