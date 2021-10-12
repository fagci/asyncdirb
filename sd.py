#!/usr/bin/env python3
from ipaddress import IPv4Address
from random import randint
from socket import IPPROTO_TCP, SOL_SOCKET, SO_LINGER, SO_REUSEADDR, TCP_NODELAY
from socket import setdefaulttimeout, socket, timeout
from struct import pack
from threading import Event, Thread

T = 'GET /wp-content/uploads/ HTTP/1.1\r\nHost: %s\r\n\r\n'
LINGER = pack('ii', 1, 0)

def scan(running_event):
    while running_event.is_set():
        ip_address = IPv4Address(randint(0x1000000, 0xE0000000))
        if ip_address.is_global:
            ip = str(ip_address)

            with socket() as s:
                s.setsockopt(IPPROTO_TCP, TCP_NODELAY, True)
                s.setsockopt(SOL_SOCKET, SO_LINGER, LINGER)
                s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

                if s.connect_ex((ip, 80)):
                    continue

                try:
                    s.send((T % ip).encode('ascii'))
                    if 'Index of' in s.recv(1024).decode('ascii', 'ignore'):
                        print('[+]', ip)
                except (ConnectionError, timeout):
                    pass


def main():
    pool = []
    running_event = Event()
    running_event.set()

    setdefaulttimeout(1)

    for _ in range(1024):
        t = Thread(target=scan, args=(running_event, ))
        t.start()
        pool.append(t)

    try:
        for t in pool:
            t.join()
    except KeyboardInterrupt:
        running_event.clear()
        print('\rInterrupt')


if __name__ == '__main__':
    main()
