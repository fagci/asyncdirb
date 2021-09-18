#!/usr/bin/env python3
from ipaddress import IPv4Address
from random import randint
from socket import IPPROTO_TCP, TCP_NODELAY, setdefaulttimeout, socket, timeout
from threading import Event, Thread

running_event = Event()
T = 'GET /wp-content/uploads/ HTTP/1.1\r\nHost: %s\r\n\r\n'


def scan():
    while running_event.is_set():
        ip_address = IPv4Address(randint(0x1000000, 0xE0000000))
        if not ip_address.is_global:
            continue

        ip = str(ip_address)

        with socket() as s:
            s.setsockopt(IPPROTO_TCP, TCP_NODELAY, True)

            if s.connect_ex((ip, 80)) == 0:
                try:
                    s.send((T % ip).encode('ascii'))
                    if b'Index of' in s.recv(1024):
                        print('[+]', ip)
                except (ConnectionError, timeout, IndexError, ValueError):
                    pass


def main():
    pool = []
    running_event.set()

    setdefaulttimeout(1)

    for _ in range(1024):
        t = Thread(target=scan)
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
