#!/usr/bin/env python3

from threading import Event, Thread
from time import sleep
from uuid import UUID, uuid4

from discovery import Discovery
from server import Protocol

DISCOVERY_INTERVAL = 1


def read_discovery(discovery, protocol, stop: Event):
    '''
    Read discovery packets from the multicast group.
    '''
    while not stop.is_set():
        read_result = discovery.read()
        if read_result is None:
            continue

        session, (addr, port) = read_result
        print('Discovered session %s from %s:%d' % (session, addr, port))

        # TODO: connect to the remote peer


def send_discovery(discovery: Discovery, stop: Event):
    '''
    Periodically send discovery packets to the multicast group.
    '''
    while not stop.is_set():
        discovery.send()
        sleep(DISCOVERY_INTERVAL)


if __name__ == '__main__':
    try:
        session = uuid4()
        print('Session %s started' % (session))

        protocol = Protocol()
        discovery = Discovery(protocol.port, session)

        stop = Event()

        discovery_recv_thread = Thread(target=read_discovery, args=(discovery, protocol, stop))
        discovery_recv_thread.start()

        discovery_send_thread = Thread(target=send_discovery, args=(discovery, stop))
        discovery_send_thread.start()

        discovery_recv_thread.join()
        discovery_send_thread.join()
    finally:
        stop.set()

        discovery.close()
        protocol.close()
