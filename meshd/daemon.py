#!/usr/bin/env python3

from threading import Event, Thread
from uuid import uuid4, UUID
from time import sleep
import argparse
import socket

from discovery.multicast import MulticastDiscovery
from protocol.connection import ProtocolConnection
from protocol.manager import ProtocolConnectionManager
from protocol.server import ProtocolServer
from transport.transport import Transport

DISCOVERY_INTERVAL = 1

def discovery_main(discovery: MulticastDiscovery,
                   local_session: UUID,
                   protocol_manager: ProtocolConnectionManager,
                   stop_event: Event):
    cache = {}
    while not stop_event.is_set():
        result = discovery.read(DISCOVERY_INTERVAL)
        if result:
            remote_session, (remote_addr, remote_port) = result

            if (remote_addr, remote_port) in cache:
                continue
            cache[(remote_addr, remote_port)] = True

            if remote_session < local_session and remote_session not in protocol_manager:
                ProtocolConnection.connect(local_session, remote_addr, remote_port, protocol_manager, stop_event)
                # protocol_manager.register_connection(remote_session, ProtocolConnection.connect(local_session, remote_addr, remote_port, protocol_manager, stop_event))

        discovery.send()

def protocol_main(local_session: UUID, manager: ProtocolConnectionManager, server: ProtocolServer, stop_event: Event):
    cache = {}

    for sock in server.accept_until_stop(stop_event):
        remote_addr, remote_port = sock.getpeername()
        print(f'Got discovery {remote_addr} and port {remote_port}')
        if (remote_addr, remote_port) in cache:
            print(f'Discovery {remote_addr} in Cache')
            continue
        cache[(remote_addr, remote_port)] = True

        # protocol_manager.register_connection(remote_session,
        #                                      ProtocolConnection.accept(local_session, sock, manager, stop_event))
        ProtocolConnection.accept(local_session, sock, manager, stop_event)

def recieve_sensor_data(local_session: UUID, server: ProtocolServer, transport: Transport, protocol_manager:ProtocolConnectionManager, stop_event: Event):
    for sock in server.accept_until_stop(stop_event):
        try:
            res = sock.recv(1024)
            if (res):
                (alert_type, data) = transport.recieve_sensor_data(res)
                protocol_manager.recieved_data(transport, alert_type, data)
        except socket.timeout:
            pass
        sleep(3)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sensorport', help='Sensor Port Specification', required=True)
    args = parser.parse_args()

    if args.sensorport is None:
        print("Please specify the type of sensor")
        exit(1)

    sensor_port = int(args.sensorport)

    session = uuid4()  # local session id
    stop = Event()  # root cancellation event

    try:
        protocol_server = ProtocolServer(None)
        # print(f'socketname : {protocol_server.server.getsockname()} and hostname : {socket.gethostname()} and addr info {socket.getaddrinfo(socket.gethostname(), protocol_server.port)}')
        protocol_manager = ProtocolConnectionManager()
        discovery = MulticastDiscovery(protocol_server.port, session)
        sensor_server = ProtocolServer(sensor_port)

        discovery_thread = Thread(target=discovery_main, args=(discovery, session, protocol_manager, stop))
        discovery_thread.start()

        protocol_accept_thread = Thread(target=protocol_main, args=(session, protocol_manager, protocol_server, stop))
        protocol_accept_thread.start()

        print(f"Local session {session} started")

        sensor_read_thread = Thread(target=recieve_sensor_data, args=(session, sensor_server, Transport(), protocol_manager, stop))
        sensor_read_thread.start()

        discovery_thread.join()
        protocol_accept_thread.join()
        sensor_read_thread.join()
    finally:
        stop.set()


if __name__ == '__main__':
    main()
