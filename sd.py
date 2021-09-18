#!/usr/bin/env python3
from ipaddress import IPv4Address
from random import randint
from socket import IPPROTO_TCP, TCP_NODELAY, setdefaulttimeout, socket, timeout
from threading import Event, Thread

T = 'GET /wp-content/uploads/ HTTP/1.1\r\nHost: %s\r\n\r\n'


def scan(running_event):
    while running_event.is_set():
        ip_address = IPv4Address(randint(0x1000000, 0xE0000000))
        if ip_address.is_global:
            ip = str(ip_address)

            with socket() as s:
                s.setsockopt(IPPROTO_TCP, TCP_NODELAY, True)

                if s.connect_ex((ip, 80)) == 0:
                    try:
                        s.send((T % ip).encode('ascii'))
                        if b'Index of' in s.recv(1024):
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
